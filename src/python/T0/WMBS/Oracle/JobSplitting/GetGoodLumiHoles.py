"""
_GetGoodLumiHoles_

Oracle implementation of GetGoodLumiHoles

For a given repack merge subscription return the
empty lumis (no streamers) or completely repacked
lumis above a provided lumi threshold.
"""

from WMCore.Database.DBFormatter import DBFormatter

class GetGoodLumiHoles(DBFormatter):

    sql = """SELECT lumi_section_closed.lumi_id AS lumi
             FROM wmbs_subscription
             INNER JOIN wmbs_workflow_output ON
               wmbs_workflow_output.output_fileset = wmbs_subscription.fileset
             INNER JOIN wmbs_subscription repack_subscription ON
               repack_subscription.workflow = wmbs_workflow_output.workflow_id
             INNER JOIN run_stream_fileset_assoc ON
               run_stream_fileset_assoc.fileset = repack_subscription.fileset
             INNER JOIN lumi_section_closed ON
               lumi_section_closed.run_id = run_stream_fileset_assoc.run_id AND
               lumi_section_closed.stream_id = run_stream_fileset_assoc.stream_id AND
               lumi_section_closed.close_time > 0 AND
               lumi_section_closed.lumi_id > :firstlumi
             LEFT OUTER JOIN streamer ON
               streamer.run_id = run_stream_fileset_assoc.run_id AND
               streamer.stream_id = run_stream_fileset_assoc.stream_id AND
               streamer.lumi_id = lumi_section_closed.lumi_id
             LEFT OUTER JOIN wmbs_sub_files_available ON
               wmbs_sub_files_available.fileid = streamer.id AND
               wmbs_sub_files_available.subscription = repack_subscription.id
             LEFT OUTER JOIN wmbs_sub_files_acquired ON
               wmbs_sub_files_acquired.fileid = streamer.id AND
               wmbs_sub_files_acquired.subscription = repack_subscription.id
             LEFT OUTER JOIN lumi_section_split_active ON
               lumi_section_split_active.run_id = run_stream_fileset_assoc.run_id AND
               lumi_section_split_active.lumi_id = lumi_section_closed.lumi_id AND
               lumi_section_split_active.subscription = repack_subscription.id
             WHERE wmbs_subscription.id = :subscription
             GROUP BY lumi_section_closed.lumi_id
             HAVING MIN(lumi_section_closed.filecount) = 0 OR
               ( MIN(lumi_section_closed.filecount) = SUM(streamer.used) AND
                 COUNT(wmbs_sub_files_available.fileid) = 0 AND
                 COUNT(wmbs_sub_files_acquired.fileid) = 0 AND
                 COUNT(lumi_section_split_active.run_id) = 0 )
             """

    def execute(self, subscription, firstlumi, conn = None, transaction = False):

        results = self.dbi.processData(self.sql, { 'subscription' : subscription,
                                                   'firstlumi' : firstlumi},
                                       conn = conn, transaction = transaction)[0].fetchall()

        lumiList = []
        for result in results:
            lumiList.append(result[0])

        return lumiList
