"""
_GetRunStreamDone_

Oracle implementation of GetRunStreamDone

Returns run/stream combinations that are fully processed

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetRunStreamDone(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT run_stream_done.run_id AS run,
                        stream.name AS stream
                 FROM run_stream_done
                 INNER JOIN stream ON
                   stream.id = run_stream_done.stream_id
                 LEFT OUTER JOIN run_stream_fileset_assoc ON
                   run_stream_fileset_assoc.run_id = run_stream_done.run_id AND
                   run_stream_fileset_assoc.stream_id = run_stream_done.stream_id
                 WHERE checkForZeroState(run_stream_done.in_datasvc) = 0
                 AND run_stream_fileset_assoc.run_id IS NULL
                 """

        results = self.dbi.processData(sql, binds = {}, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)
