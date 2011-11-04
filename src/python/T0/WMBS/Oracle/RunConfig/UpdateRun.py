"""
_UpdateRun_

Oracle implementation of UpdateRun

"""

from WMCore.Database.DBFormatter import DBFormatter

class UpdateRun(DBFormatter):

    def execute(self, run, process, acqEra,
                recoTimeout, recoLockTimeout,
                conn = None, transaction = False):

        sql = """UPDATE run
                 SET process = :p_1,
                     acq_era = :p_2,
                     reco_timeout = :p_3,
                     reco_lock_timeout = :p_4
                 WHERE run_id = :p_5
                 """

        binds = { 'p_1' : process,
                  'p_2' : acqEra,
                  'p_3' : recoTimeout,
                  'p_4' : recoLockTimeout,
                  'p_5' : run }

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
