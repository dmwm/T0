"""
_GetRunInfo_

Oracle implementation of GetRunInfo

Retrieve information about run from online sources

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetRunInfo(DBFormatter):

    def execute(self, run, conn = None, transaction = False):

        hltkey = None
        cmssw_version = None

        binds = { 'RUN' : run }

        sql = """SELECT CMS_HLT_GDR.U_CONFVERSIONS.NAME AS hltkey
                 FROM CMS_HLT_GDR.U_CONFVERSIONS
                 INNER JOIN CMS_WBM.RUNSUMMARY ON
                   CMS_WBM.RUNSUMMARY.HLTKEY = CMS_HLT_GDR.U_CONFVERSIONS.CONFIGID
                 WHERE CMS_WBM.RUNSUMMARY.RUNNUMBER = :RUN
                 """
        
        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)[0].fetchall()

        if len(results) == 1:
            hltkey = results[0][0]

        sql = """SELECT STRING_VALUE as cmssw_version
                 FROM CMS_RUNINFO.RUNSESSION_PARAMETER
                 WHERE NAME='CMS.DAQ:CMSSW_VERSION'
                 AND RUNNUMBER = :RUN
                 """

        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)[0].fetchall()

        if len(results) == 1:
            cmssw_version = results[0][0]

        return (hltkey, cmssw_version)
