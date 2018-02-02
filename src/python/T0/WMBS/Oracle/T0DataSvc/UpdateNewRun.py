"""
_UpdateNewRun_

Oracle implementation of UpdateNewRun

Mark run info as present in in Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class UpdateNewRun(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """UPDATE run
                 SET in_datasvc = 1
                 WHERE run_id = :RUN
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
