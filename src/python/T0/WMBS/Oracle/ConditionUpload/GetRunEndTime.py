"""
_GetRunEndTime_

Oracle implementation of GetRunEndTime

Returns run end time or insert time of last
streamer if run hasn't ended yet.

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetRunEndTime(DBFormatter):

    def execute(self, run, conn = None, transaction = False):

        sql = """SELECT CASE
                          WHEN run.end_time > 0 THEN run.end_time
                          ELSE (SELECT MAX(streamer.insert_time)
                                FROM streamer
                                WHERE streamer.run_id = :RUN)
                        END
                 FROM run
                 WHERE run.run_id = :RUN
                 """

        endTime = self.dbi.processData(sql, { 'RUN' : run },
                                       conn = conn, transaction = transaction)[0].fetchall()[0][0]

        return endTime
