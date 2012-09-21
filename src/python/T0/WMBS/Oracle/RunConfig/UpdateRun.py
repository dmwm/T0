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
                     lfn_base = :LFNBASE,
                     ah_timeout = :AHTIMEOUT,
                     ah_dir = :AHDIR
                 WHERE run_id = :RUN
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
