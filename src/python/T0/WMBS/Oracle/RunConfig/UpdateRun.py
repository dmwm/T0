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
                     lfn_prefix = :LFNPREFIX,
                     bulk_data_type = :BULKDATATYPE,
                     bulk_data_loc = :BULKDATALOC,
                     ah_timeout = :AHTIMEOUT,
                     ah_dir = :AHDIR,
                     cond_timeout = :CONDTIMEOUT,
                     db_host = :DBHOST,
                     valid_mode = :VALIDMODE
                 WHERE run_id = :RUN
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
