"""
_EndRuns_

Oracle implementation of EndRuns

Updates the specified runs to ended in T0AST,
sets both end time and lumi count for each run.

"""
import time

from WMCore.Database.DBFormatter import DBFormatter

class EndRuns(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """UPDATE run
                 SET end_time = :END_TIME,
                     lumicount = :LUMICOUNT
                 WHERE run_id = :RUN
                 """

        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)

        return
