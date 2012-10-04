"""
_MarkRepackInjected_

Oracle implementation of MarkRepackInjected

Check that all datasets for a workflow (ie. stream)
have had their PromptReco released and then mark
the repack workflow as injected

"""

from WMCore.Database.DBFormatter import DBFormatter

class MarkRepackInjected(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """UPDATE wmbs_workflow
                 SET injected = 1
                 WHERE name in (
                   SELECT wmbs_workflow.name
                   FROM run_stream_fileset_assoc
                     INNER JOIN wmbs_subscription ON
                       wmbs_subscription.fileset = run_stream_fileset_assoc.fileset
                     INNER JOIN wmbs_workflow ON
                       wmbs_workflow.id = wmbs_subscription.workflow AND
                       wmbs_workflow.injected = 0
                     INNER JOIN run_primds_stream_assoc ON
                       run_primds_stream_assoc.run_id = run_stream_fileset_assoc.run_id AND
                       run_primds_stream_assoc.stream_id =   run_stream_fileset_assoc.stream_id
                     LEFT OUTER JOIN reco_config ON
                       reco_config.run_id = run_stream_fileset_assoc.run_id AND
                       reco_config.primds_id = run_primds_stream_assoc.primds_id
                   GROUP BY wmbs_workflow.name
                   HAVING COUNT(reco_config.run_id) = COUNT(*)
                 )
                 """

        self.dbi.processData(sql, binds = {}, conn = conn,
                             transaction = transaction)

        return
