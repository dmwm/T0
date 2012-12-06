"""
_GetCompletedLumisFromChildSub_

Oracle implementation of GetCompletedLumis

For a given repack merge subscription return the
completely repacked lumis above a provided lumi
threshold.
"""

from WMCore.Database.DBFormatter import DBFormatter

class GetCompletedLumisFromChildSub(DBFormatter):

    sql = """SELECT streamer.lumi_id
             FROM run_stream_fileset_assoc
             INNER JOIN lumi_section_closed ON
               lumi_section_closed.run_id = run_stream_fileset_assoc.run_id AND
               lumi_section_closed.stream_id = run_stream_fileset_assoc.stream_id AND
               lumi_section_closed.lumi_id > :firstlumi AND
               lumi_section_closed.close_time > 0 AND
               lumi_section_closed.filecount > 0
             INNER JOIN wmbs_subscription parent_subscription ON
               parent_subscription.fileset = run_stream_fileset_assoc.fileset
             INNER JOIN wmbs_workflow_output ON
               wmbs_workflow_output.workflow_id = parent_subscription.workflow
             INNER JOIN wmbs_subscription child_subscription ON
               child_subscription.fileset = wmbs_workflow_output.output_fileset AND
               child_subscription.id = :subscription
             INNER JOIN streamer ON
               streamer.run_id = run_stream_fileset_assoc.run_id AND
               streamer.stream_id = run_stream_fileset_assoc.stream_id AND
               streamer.lumi_id = lumi_section_closed.lumi_id
             LEFT OUTER JOIN wmbs_sub_files_available ON
               wmbs_sub_files_available.fileid = streamer.id AND
               wmbs_sub_files_available.subscription = parent_subscription.id
             LEFT OUTER JOIN wmbs_sub_files_acquired ON
               wmbs_sub_files_acquired.fileid = streamer.id AND
               wmbs_sub_files_acquired.subscription = parent_subscription.id
             GROUP BY streamer.lumi_id
             HAVING COUNT(*) = SUM(streamer.used)
             AND COUNT(wmbs_sub_files_available.fileid) = 0
             AND COUNT(wmbs_sub_files_acquired.fileid) = 0
             """

    def execute(self, subscription, firstlumi, conn = None, transaction = False):

        results = self.dbi.processData(self.sql, { 'subscription' : subscription,
                                                   'firstlumi' : firstlumi},
                                       conn = conn, transaction = transaction)[0].fetchall()

        lumiList = []
        for result in results:
            lumiList.append(result[0])

        return lumiList
