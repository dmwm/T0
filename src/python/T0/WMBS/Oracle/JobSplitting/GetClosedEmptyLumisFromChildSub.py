"""
_GetClosedEmptyLumisFromChildSub_

Oracle implementation of GetClosedEmptyLumis

For a given repack merge subscription return the
closed, but empty lumis in it's input data. Only
look at lumis above a provided lumi threshold.
"""

from WMCore.Database.DBFormatter import DBFormatter

class GetClosedEmptyLumisFromChildSub(DBFormatter):

    sql = """SELECT lumi_section_closed.lumi_id
             FROM run_stream_fileset_assoc
             INNER JOIN lumi_section_closed ON
               lumi_section_closed.run_id = run_stream_fileset_assoc.run_id AND
               lumi_section_closed.stream_id = run_stream_fileset_assoc.stream_id AND
               lumi_section_closed.close_time > 0 AND
               lumi_section_closed.lumi_id > :firstlumi AND
               lumi_section_closed.filecount = 0
             INNER JOIN wmbs_subscription parent_subscription ON
               parent_subscription.fileset = run_stream_fileset_assoc.fileset
             INNER JOIN wmbs_workflow_output ON
               wmbs_workflow_output.workflow_id = parent_subscription.workflow
             INNER JOIN wmbs_subscription child_subscription ON
               child_subscription.fileset = wmbs_workflow_output.output_fileset
             WHERE child_subscription.id = :subscription
             """

    def execute(self, subscription, firstlumi, conn = None, transaction = False):

        results = self.dbi.processData(self.sql, { 'subscription' : subscription,
                                                   'firstlumi' : firstlumi },
                                       conn = conn, transaction = transaction)[0].fetchall()

        lumiList = []
        for result in results:
            lumiList.append(result[0])

        return lumiList
