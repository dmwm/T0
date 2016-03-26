"""
_CloseRuns_

Oracle implementation of CloseRuns

Updates the specified runs to closed in T0AST,
sets both close time and lumi count for each run.

"""
import time

from WMCore.Database.DBFormatter import DBFormatter

class CloseRuns(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """UPDATE run
                 SET close_time = :CLOSE_TIME,
                     lumicount = :LUMICOUNT
                 WHERE run_id = :RUN
                 """

        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)

        return
