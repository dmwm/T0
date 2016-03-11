"""
_GetLumiHolesForRepackMerge_

Oracle implementation of GetLumiHolesForRepackMerge

For a given repack merge subscription return the empty lumis (no streamers)
"""

from WMCore.Database.DBFormatter import DBFormatter

class GetLumiHolesForRepackMerge(DBFormatter):

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
               lumi_section_closed.filecount = 0
             WHERE wmbs_subscription.id = :subscription
             """

    def execute(self, subscription, conn = None, transaction = False):

        results = self.dbi.processData(self.sql, { 'subscription' : subscription },
                                       conn = conn, transaction = transaction)[0].fetchall()

        lumiSet = set()
        for result in results:
            lumiSet.add(result[0])

        return lumiSet
