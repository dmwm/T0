"""
_FindNewRunStreams_

Oracle implementation of FindNewRunStreams

Returns a dictionary of run:streams for all run
and stream combinations that are not configured.

"""

from WMCore.Database.DBFormatter import DBFormatter

class FindNewRunStreams(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT run_stream_cmssw_assoc.run_id,
                        stream.name
                 FROM run_stream_cmssw_assoc
                 INNER JOIN run ON
                   run.run_id = run_stream_cmssw_assoc.run_id AND
                   run.acq_era IS NOT NULL
                 LEFT OUTER JOIN run_stream_style_assoc ON
                   run_stream_style_assoc.run_id = run_stream_cmssw_assoc.run_id AND
                   run_stream_style_assoc.stream_id = run_stream_cmssw_assoc.stream_id
                 INNER JOIN stream ON
                   stream.id = run_stream_cmssw_assoc.stream_id
                 WHERE run_stream_style_assoc.run_id IS NULL
                 """

        results = self.dbi.processData(sql, {}, conn = conn,
                                       transaction = transaction)[0].fetchall()

        runStreams = {}
        for result in results:
            run = result[0]
            stream = result[1]
            if run not in runStreams:
                runStreams[run] = []
            runStreams[run].append(stream)

        return runStreams
