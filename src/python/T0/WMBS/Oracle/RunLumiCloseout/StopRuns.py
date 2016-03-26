"""
_StopRuns_

Oracle implementation of StopRuns

Updates the specified runs to stopped in T0AST,
sets both start time and stop time for each run.

"""
import time

from WMCore.Database.DBFormatter import DBFormatter

class StopRuns(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """UPDATE run
                 SET start_time = :START_TIME,
                     stop_time = :STOP_TIME
                 WHERE run_id = :RUN
                 """

        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)

        return
