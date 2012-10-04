"""
_FindActiveRuns_

Oracle implementation of FindActiveRuns

Return a list of all active runs (end_time is 0).

"""

from WMCore.Database.DBFormatter import DBFormatter

class FindActiveRuns(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT run_id
                 FROM run
                 WHERE end_time = 0
                 """

        results = self.dbi.processData(sql, {}, conn = conn,
                                       transaction = transaction)[0].fetchall()

        runs = []
        for result in results:
            runs.append(result[0])

        return runs
