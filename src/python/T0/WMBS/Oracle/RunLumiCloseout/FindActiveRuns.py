"""
_FindActiveRuns_

Oracle implementation of FindActiveRuns

Return a list of all active runs

For replays wait til the run is closed and then update
start_time and stop_time with the MIN and MAX streamer
insert_time for the run
"""

from WMCore.Database.DBFormatter import DBFormatter

class FindActiveRuns(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT run_id,
                        close_time,
                        backfill
                 FROM run
                 WHERE stop_time = 0
                 AND acq_era IS NOT NULL
                 """

        results = self.dbi.processData(sql, {}, conn = conn,
                                       transaction = transaction)[0].fetchall()

        binds = []
        returnRuns = []
        for result in results:
            if not result[2]:
                returnRuns.append(result[0])
            elif result[1] > 0:
                binds.append( { 'RUN' : result[0] } )

        if len(binds) > 0:

            sql = """UPDATE run
                     SET start_time = (SELECT MIN(insert_time)
                                       FROM streamer
                                       WHERE run_id = :RUN),
                         stop_time = (SELECT MAX(insert_time)
                                      FROM streamer
                                      WHERE run_id = :RUN)
                     WHERE run_id = :RUN
                     """

            self.dbi.processData(sql, binds, conn = conn,
                                 transaction = transaction)

        return returnRuns
