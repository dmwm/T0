"""
_GetRunInfo_

Oracle implementation of GetRunInfo

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetRunInfo(DBFormatter):

    def execute(self, run, conn = None, transaction = False):

        sql = """SELECT status,
                        hltkey,
                        process,
                        acq_era,
                        lfn_base,
                        ah_timeout,
                        ah_dir
                 FROM run
                 WHERE run_id = :RUN
                 """

        binds = { 'RUN' : run }
        
        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)
