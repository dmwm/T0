"""
_GetRunInfo_

Oracle implementation of GetRunInfo

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetRunInfo(DBFormatter):

    def execute(self, run, conn = None, transaction = False):

        sql = """SELECT status,
                        hltkey,
                        reco_timeout,
                        reco_lock_timeout,
                        process,
                        acq_era
                 FROM run
                 WHERE run_id = :RUN
                 """

        binds = { 'RUN' : run }
        
        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)
