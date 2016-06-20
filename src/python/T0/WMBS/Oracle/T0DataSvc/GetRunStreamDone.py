"""
_GetRunStreamDone_

Oracle implementation of GetRunStreamDone

Returns run/stream combinations that are fully processed

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetRunStreamDone(DBFormatter):

    def execute(self, conn = None, transaction = False):

        returnList = []

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
                                       transaction = transaction)[0].fetchall()

        for result in results:
            returnList.append( { 'run': result[0],
                                 'stream': result[1] } )

        sql = """SELECT run_stream_done.run_id AS run,
                        stream.name AS stream
                 FROM run_stream_done
                 INNER JOIN stream ON
                   stream.id = run_stream_done.stream_id
                 INNER JOIN run_stream_fileset_assoc ON
                   run_stream_fileset_assoc.run_id = run_stream_done.run_id AND
                   run_stream_fileset_assoc.stream_id = run_stream_done.stream_id
                 INNER JOIN wmbs_subscription ON
                   wmbs_subscription.fileset = run_stream_fileset_assoc.fileset
                 INNER JOIN wmbs_workflow ON
                   wmbs_workflow.id = wmbs_subscription.workflow
                 INNER JOIN wmbs_workflow runstream_workflow ON
                   runstream_workflow.name = wmbs_workflow.name
                 INNER JOIN wmbs_subscription runstream_subscription ON
                   runstream_subscription.workflow = runstream_workflow.id
                 WHERE checkForZeroState(run_stream_done.in_datasvc) = 0
                 GROUP BY run_stream_done.run_id,
                          stream.name
                 HAVING SUM(runstream_subscription.finished) = COUNT(*)
                 """

        results = self.dbi.processData(sql, binds = {}, conn = conn,
                                       transaction = transaction)[0].fetchall()

        for result in results:
            returnList.append( { 'run': result[0],
                                 'stream': result[1] } )

        return returnList
