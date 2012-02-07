"""
_FindNewRunStreams_

Oracle implementation of FindNewRunStreams

Returns a dictionary of run:streams for all run
and stream combinations that are not configured.

"""

from WMCore.Database.DBFormatter import DBFormatter

class FindNewRunStreams(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT streamer.run_id, stream.name
                 FROM streamer
                 INNER JOIN run ON
                   run.run_id = streamer.run_id AND
                   run.acq_era IS NOT NULL
                 LEFT OUTER JOIN run_stream_fileset_assoc ON
                   run_stream_fileset_assoc.run_id = streamer.run_id AND
                   run_stream_fileset_assoc.stream_id = streamer.stream_id
                 INNER JOIN stream ON
                   stream.id = streamer.stream_id
                 WHERE checkForZeroState(streamer.used) = 0
                 AND run_stream_fileset_assoc.run_id IS NULL
                 GROUP BY streamer.run_id, stream.name
                 """

        results = self.dbi.processData(sql, {}, conn = conn,
                                       transaction = transaction)[0].fetchall()

        runStreams = {}
        for result in results:
            run = result[0]
            stream = result[1]
            if not runStreams.has_key(run):
                runStreams[run] = []
            runStreams[run].append(stream)

        return runStreams
