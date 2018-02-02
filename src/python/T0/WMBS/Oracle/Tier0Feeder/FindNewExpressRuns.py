"""
_FindNewExpressRuns_

Oracle implementation of FindNewExpressRuns

Return all runs that haven't had Express released

"""

from WMCore.Database.DBFormatter import DBFormatter

class FindNewExpressRuns(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT run.run_id
                 FROM run
                 WHERE checkForZeroState(run.express_released) = 0
                 """

        results = self.dbi.processData(sql, {}, conn = conn,
                                       transaction = transaction)[0].fetchall()

        runs = []
        for result in results:
            runs.append(result[0])

        return runs
