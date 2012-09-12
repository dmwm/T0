"""
_UpdateRun_

Oracle implementation of UpdateRun

"""

from WMCore.Database.DBFormatter import DBFormatter

class UpdateRun(DBFormatter):

    def execute(self, run, lfnBase, process, acqEra,
                conn = None, transaction = False):

        sql = """UPDATE run
                 SET lfn_base = :p_1,
                     process = :p_2,
                     acq_era = :p_3
                 WHERE run_id = :p_4
                 """

        binds = { 'p_1' : lfnBase,
                  'p_2' : process,
                  'p_3' : acqEra,
                  'p_4' : run }

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
