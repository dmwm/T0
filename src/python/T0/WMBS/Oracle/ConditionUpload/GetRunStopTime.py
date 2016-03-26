"""
_GetRunStopTime_

Oracle implementation of GetRunStopTime

Returns run stop time or insert time of last
streamer if run hasn't stopped  yet.

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetRunStopTime(DBFormatter):

    def execute(self, run, conn = None, transaction = False):

        sql = """SELECT CASE
                          WHEN run.stop_time > 0 THEN run.stop_time
                          ELSE (SELECT MAX(streamer.insert_time)
                                FROM streamer
                                WHERE streamer.run_id = :RUN)
                        END
                 FROM run
                 WHERE run.run_id = :RUN
                 """

        stopTime = self.dbi.processData(sql, { 'RUN' : run },
                                        conn = conn, transaction = transaction)[0].fetchall()[0][0]

        return stopTime
