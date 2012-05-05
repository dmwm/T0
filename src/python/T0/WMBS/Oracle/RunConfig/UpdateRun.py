"""
_UpdateRun_

Oracle implementation of UpdateRun

"""

from WMCore.Database.DBFormatter import DBFormatter

class UpdateRun(DBFormatter):

    def execute(self, run, process, acqEra,
                conn = None, transaction = False):

        sql = """UPDATE run
                 SET process = :p_1,
                     acq_era = :p_2
                 WHERE run_id = :p_3
                 """

        binds = { 'p_1' : process,
                  'p_2' : acqEra,
                  'p_3' : run }

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
