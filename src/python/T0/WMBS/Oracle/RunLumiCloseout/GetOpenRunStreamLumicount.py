"""
_GetOpenRunStreamLumicount_

Oracle implementation of GetOpenRunStreamLumicount

Return the lumicount for all all closed runs with open run/stream filesets

"""
import time

from WMCore.Database.DBFormatter import DBFormatter

class GetOpenRunStreamLumicount(DBFormatter):

    sql = """SELECT run_stream_fileset_assoc.run_id AS run,
                    MAX(run.lumicount) AS lumicount
             FROM run_stream_fileset_assoc
             INNER JOIN wmbs_fileset ON
               wmbs_fileset.id = run_stream_fileset_assoc.fileset AND
               wmbs_fileset.open = 1
             INNER JOIN run ON
               run.run_id = run_stream_fileset_assoc.run_id AND
               run.stop_time > 0 AND
               run.close_time > 0
             GROUP BY run_stream_fileset_assoc.run_id
             """

    def execute(self, conn = None, transaction = False):

        results = self.dbi.processData(self.sql, binds = {},
                                       conn = conn, transaction = transaction)[0].fetchall()

        runInfo = {}
        for result in results:
            runInfo[result[0]] = result[1]

        return runInfo
