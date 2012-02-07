"""
_FindNewRuns_

Oracle implementation of FindNewRuns

Return a dictionary of run:hltkey for all runs
that are not configured.

"""

from WMCore.Database.DBFormatter import DBFormatter

class FindNewRuns(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT run_id, hltkey
                 FROM run
                 WHERE acq_era IS NULL
                 """

        results = self.dbi.processData(sql, {}, conn = conn,
                                       transaction = transaction)[0].fetchall()

        runHltkeys = {}
        for result in results:
            runHltkeys[result[0]] = result[1]

        return runHltkeys
