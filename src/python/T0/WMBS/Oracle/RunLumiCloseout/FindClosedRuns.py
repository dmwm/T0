"""
_FindClosedRuns_

Oracle implementation of FindClosedRuns

Checks the given runs whether they are closed according to
the StorageManager EoR records and returns a list of all
closed runs together with the high lumi section for each run.

"""

from WMCore.Database.DBFormatter import DBFormatter

class FindClosedRuns(DBFormatter):

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

        closedRuns = {}
        for result in results:
            closedRuns[result[0]] = result[1]

        return closedRuns
