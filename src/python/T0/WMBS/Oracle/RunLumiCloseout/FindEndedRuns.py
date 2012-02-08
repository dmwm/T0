"""
_FindEndedRuns_

Oracle implementation of FindActiveRuns

Checks the given runs whether the have ended according to
the StorageManager EoR records and returns a list of all
ended runs together with the high lumi section for each run.

"""

from WMCore.Database.DBFormatter import DBFormatter

class FindEndedRuns(DBFormatter):

    def execute(self, runs, conn = None, transaction = False):

        sql = """SELECT a.runnumber, MAX(a.n_lumisections)
                 FROM CMS_STOMGR.runs a
                 WHERE a.runnumber = :RUN
                 AND a.status = 0
                 GROUP BY a.runnumber
                 HAVING COUNT(*) = MAX(a.n_instances)
                 """

        binds = []
        for run in runs:
            binds.append( { 'RUN' : run } )

        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)[0].fetchall()

        endedRuns = {}
        for result in results:
            endedRuns[result[0]] = result[1]

        return endedRuns
