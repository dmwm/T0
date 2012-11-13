"""
_GetRunInfo_

Oracle implementation of GetRunInfo

Return global information for given run (from run table).

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetRunInfo(DBFormatter):

    def execute(self, run, conn = None, transaction = False):

        sql = """SELECT status,
                        hltkey,
                        process,
                        acq_era,
                        lfn_prefix,
                        bulk_data_type,
                        bulk_data_loc,
                        ah_timeout,
                        ah_dir,
                        cond_timeout,
                        db_host,
                        valid_mode
                 FROM run
                 WHERE run_id = :RUN
                 """

        binds = { 'RUN' : run }
        
        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)
