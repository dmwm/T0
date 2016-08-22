"""
_FindStoppedRuns_

Oracle implementation of FindStoppedRuns

Checks RunSummary start and stop times for the the given runs
and returns them if both are greater than null.

"""

from WMCore.Database.DBFormatter import DBFormatter

class FindStoppedRuns(DBFormatter):

    def execute(self, runs, conn = None, transaction = False):

        sql = """SELECT runnumber,
                        (EXTRACT(DAY FROM start_interval)  * 86400) +
                        (EXTRACT(HOUR FROM start_interval) * 3600) +
                        (EXTRACT(MINUTE FROM start_interval) * 60) +
                        (EXTRACT(SECOND FROM start_interval)) AS starttime,
                        (EXTRACT(DAY FROM stop_interval)  * 86400) +
                        (EXTRACT(HOUR FROM stop_interval) * 3600) +
                        (EXTRACT(MINUTE FROM stop_interval) * 60) +
                        (EXTRACT(SECOND FROM stop_interval)) AS stoptime
                 FROM (
                   SELECT (RUNSUMMARY.starttime - TO_TIMESTAMP('01/01/1970 00:00:00', 'DD/MM/YYYY HH24:MI:SS')) AS start_interval,
                          (RUNSUMMARY.stoptime - TO_TIMESTAMP('01/01/1970 00:00:00', 'DD/MM/YYYY HH24:MI:SS')) AS stop_interval,
                          RUNSUMMARY.runnumber AS runnumber
                   FROM CMS_WBM.RUNSUMMARY
                   WHERE RUNSUMMARY.runnumber = :RUN
                   AND RUNSUMMARY.starttime IS NOT NULL
                   AND RUNSUMMARY.stoptime IS NOT NULL
                 )
                 """

        binds = []
        for run in runs:
            binds.append( { 'RUN' : run } )

        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)[0].fetchall()

        stoppedRuns = {}
        for result in results:
            stoppedRuns[result[0]] = (result[1], result[2])

        return stoppedRuns
