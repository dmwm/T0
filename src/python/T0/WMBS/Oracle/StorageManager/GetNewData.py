"""
_GetNewData_

Oracle implementation of GetNewData

Retrieve new data from StorageManager db

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetNewData(DBFormatter):

    def execute(self, minRun = None, maxRun = None, injectRun = None, conn = None, transaction = False):

        if injectRun:
            binds = { 'RUN': injectRun }
            whereSql = """WHERE CMS_STOMGR.FILE_TRANSFER_STATUS.STATUS_FLAG >= 2
                          AND CMS_STOMGR.FILE_TRANSFER_STATUS.INJECT_FLAG = 1
                          AND CMS_STOMGR.FILE_TRANSFER_STATUS.BAD_CHECKSUM = 0
                          AND CMS_STOMGR.FILE_TRANSFER_STATUS.RUNNUMBER = :RUN
                          """
        else:
            binds = {}
            whereSql = """WHERE CMS_STOMGR.T0_NEEDS_TO_INJECT(CMS_STOMGR.FILE_TRANSFER_STATUS.STATUS_FLAG,
                                                     CMS_STOMGR.FILE_TRANSFER_STATUS.INJECT_FLAG,
                                                     CMS_STOMGR.FILE_TRANSFER_STATUS.BAD_CHECKSUM) = 0
                          """
            if minRun:
                binds['MINRUN'] = minRun
                whereSql += """AND CMS_STOMGR.FILE_TRANSFER_STATUS.RUNNUMBER >= :MINRUN
                               """
            if maxRun:
                binds['MAXRUN'] = maxRun
                whereSql += """AND CMS_STOMGR.FILE_TRANSFER_STATUS.RUNNUMBER <= :MAXRUN
                               """

        sql = """SELECT CMS_STOMGR.FILE_TRANSFER_STATUS.FILE_ID AS p5_id,
                        CMS_STOMGR.FILE_TRANSFER_STATUS.RUNNUMBER AS run,
                        CMS_STOMGR.FILE_TRANSFER_STATUS.LS AS lumi,
                        CMS_STOMGR.FILE_TRANSFER_STATUS.STREAM AS stream,
                        CMS_STOMGR.FILE_TRANSFER_STATUS.PATH AS path,
                        CMS_STOMGR.FILE_TRANSFER_STATUS.FILENAME AS filename,
                        CMS_STOMGR.FILE_QUALITY_CONTROL.FILE_SIZE AS filesize,
                        NVL(CMS_STOMGR.FILE_QUALITY_CONTROL.EVENTS_ACCEPTED, 0) AS events
                 FROM CMS_STOMGR.FILE_TRANSFER_STATUS
                 INNER JOIN CMS_STOMGR.FILE_QUALITY_CONTROL ON
                   CMS_STOMGR.FILE_QUALITY_CONTROL.FILENAME = CMS_STOMGR.FILE_TRANSFER_STATUS.FILENAME
                 %s
                 AND CMS_STOMGR.FILE_TRANSFER_STATUS.PATH IS NOT NULL
                 AND CMS_STOMGR.FILE_QUALITY_CONTROL.FILE_SIZE IS NOT NULL
                 AND CMS_STOMGR.FILE_QUALITY_CONTROL.FILE_SIZE > 0
                 """ % whereSql

        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)
