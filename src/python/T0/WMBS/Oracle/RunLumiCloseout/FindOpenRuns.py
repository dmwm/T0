"""
_FindOpenRuns_

Oracle implementation of FindOpenRuns

Return a list of all open runs

"""

from WMCore.Database.DBFormatter import DBFormatter

class FindOpenRuns(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT run_id
                 FROM run
                 WHERE close_time = 0
                 """

        results = self.dbi.processData(sql, {}, conn = conn,
                                       transaction = transaction)[0].fetchall()

        runs = []
        for result in results:
            runs.append(result[0])

        return runs
