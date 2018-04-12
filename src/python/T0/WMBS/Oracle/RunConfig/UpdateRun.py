"""
_UpdateRun_

Oracle implementation of UpdateRun

"""

from WMCore.Database.DBFormatter import DBFormatter

class UpdateRun(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """UPDATE run
                 SET process = :PROCESS,
                     acq_era = :ACQERA,
                     backfill = :BACKFILL,
                     bulk_data_type = :BULKDATATYPE,
                     dqmuploadurl = :DQMUPLOADURL,
                     ah_timeout = :AHTIMEOUT,
                     ah_cond_lfnbase = :AHCONDLFNBASE,
                     ah_lumi_url = :AHLUMIURL,
                     cond_timeout = :CONDTIMEOUT,
                     db_host = :DBHOST,
                     valid_mode = :VALIDMODE
                 WHERE run_id = :RUN
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
