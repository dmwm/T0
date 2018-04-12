"""
_GetRunInfo_

Oracle implementation of GetRunInfo

Return global information for given run (from run table).

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetRunInfo(DBFormatter):

    def execute(self, run, conn = None, transaction = False):

        sql = """SELECT run.status AS status,
                        run.hltkey AS hltkey,
                        run.process AS process,
                        run.acq_era AS acq_era,
                        run.backfill AS backfill,
                        run.bulk_data_type AS bulk_data_type,
                        run.dqmuploadurl AS dqmuploadurl,
                        run.ah_timeout AS ah_timeout,
                        run.ah_cond_lfnbase AS ah_cond_lfnbase,
                        run.ah_lumi_url AS ah_lumi_url,
                        run.cond_timeout AS cond_timeout,
                        run.db_host AS db_host,
                        run.valid_mode AS valid_mode
                 FROM run
                 WHERE run.run_id = :RUN
                 """

        binds = { 'RUN' : run }
        
        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)
