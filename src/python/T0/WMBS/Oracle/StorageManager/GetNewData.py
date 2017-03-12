"""
_GetNewData_

Oracle implementation of GetNewData

Retrieve new data from StorageManager db

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetNewData(DBFormatter):

    def execute(self, run = None, conn = None, transaction = False):

        if run:
            binds = { 'RUN': run }
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

        sql = """SELECT CMS_STOMGR.FILE_TRANSFER_STATUS.FILE_ID AS p5_id,
                        CMS_STOMGR.FILE_TRANSFER_STATUS.RUNNUMBER AS run,
                        CMS_STOMGR.FILE_TRANSFER_STATUS.LS AS lumi,
                        CMS_STOMGR.FILE_TRANSFER_STATUS.STREAM AS stream,
                        CMS_STOMGR.FILE_TRANSFER_STATUS.PATH AS path,
                        CMS_STOMGR.FILE_TRANSFER_STATUS.FILENAME AS filename,
                        CMS_STOMGR.FILE_QUALITY_CONTROL.FILE_SIZE AS filesize,
                        CMS_STOMGR.FILE_QUALITY_CONTROL.EVENTS_BUILT AS events
                 FROM CMS_STOMGR.FILE_TRANSFER_STATUS
                 INNER JOIN CMS_STOMGR.FILE_QUALITY_CONTROL ON
                   CMS_STOMGR.FILE_QUALITY_CONTROL.FILENAME = CMS_STOMGR.FILE_TRANSFER_STATUS.FILENAME
                 %s
                 """ % whereSql

        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)
