"""
_MarkWorkflowsInjected_

Oracle implementation of MarkWorkflowsInjected

Implementation depends on whether we assume streamer
notifications to P5 or not.

with P5 streamer notifications:

 - Express sets a workflow to injected when the fileset
   is closed and all streamers are fed into the Tier0
 - Repack has the same requirements and in additions
   all datasets for that workflow/stream had their
   PromptReco released

without P5 streamer notifications:
 - Express is set to injected immediately
 - Repack needs all datasets for that workflow/stream
   PromptReco released before the workflow is set
   to injected

"""

from WMCore.Database.DBFormatter import DBFormatter

class MarkWorkflowsInjected(DBFormatter):

    sqlExpressNotify = \
       """UPDATE wmbs_workflow
          SET injected = 1
          WHERE name in (
            SELECT wmbs_workflow.name
            FROM run_stream_fileset_assoc
              INNER JOIN wmbs_subscription ON
                wmbs_subscription.fileset = run_stream_fileset_assoc.fileset
              INNER JOIN wmbs_fileset ON
                wmbs_fileset.id = wmbs_subscription.fileset AND
                wmbs_fileset.open = 0
              INNER JOIN wmbs_workflow ON
                wmbs_workflow.id = wmbs_subscription.workflow AND
                wmbs_workflow.injected = 0
              INNER JOIN run_stream_style_assoc ON
                run_stream_style_assoc.run_id = run_stream_fileset_assoc.run_id AND
                run_stream_style_assoc.stream_id =   run_stream_fileset_assoc.stream_id AND
                run_stream_style_assoc.style_id = (SELECT id FROM processing_style WHERE name = 'Express')
              LEFT OUTER JOIN streamer ON
                streamer.run_id = run_stream_fileset_assoc.run_id AND
                streamer.stream_id = run_stream_fileset_assoc.stream_id AND
                checkForZeroState(streamer.deleted) = 0
            WHERE streamer.run_id IS NULL
            GROUP BY wmbs_workflow.name
          )
          """

    sqlRepackNotify = \
       """UPDATE wmbs_workflow
          SET injected = 1
          WHERE name in (
            SELECT wmbs_workflow.name
            FROM run_stream_fileset_assoc
              INNER JOIN wmbs_subscription ON
                wmbs_subscription.fileset = run_stream_fileset_assoc.fileset
              INNER JOIN wmbs_fileset ON
                wmbs_fileset.id = wmbs_subscription.fileset AND
                wmbs_fileset.open = 0
              INNER JOIN wmbs_workflow ON
                wmbs_workflow.id = wmbs_subscription.workflow AND
                wmbs_workflow.injected = 0
              INNER JOIN run_stream_style_assoc ON
                run_stream_style_assoc.run_id = run_stream_fileset_assoc.run_id AND
                run_stream_style_assoc.stream_id =   run_stream_fileset_assoc.stream_id AND
                run_stream_style_assoc.style_id = (SELECT id FROM processing_style WHERE name = 'Bulk')
              LEFT OUTER JOIN streamer ON
                streamer.run_id = run_stream_fileset_assoc.run_id AND
                streamer.stream_id = run_stream_fileset_assoc.stream_id AND
                checkForZeroState(streamer.deleted) = 0
              INNER JOIN run_primds_stream_assoc ON
                run_primds_stream_assoc.run_id = run_stream_fileset_assoc.run_id AND
                run_primds_stream_assoc.stream_id =   run_stream_fileset_assoc.stream_id
              LEFT OUTER JOIN reco_config ON
                reco_config.run_id = run_stream_fileset_assoc.run_id AND
                reco_config.primds_id = run_primds_stream_assoc.primds_id
            WHERE streamer.run_id IS NULL
            GROUP BY wmbs_workflow.name
            HAVING COUNT(reco_config.run_id) = COUNT(*)
          )
          """

    sqlExpressNoNotify = \
       """UPDATE wmbs_workflow
          SET injected = 1
          WHERE name in (
            SELECT wmbs_workflow.name
            FROM run_stream_fileset_assoc
              INNER JOIN wmbs_subscription ON
                wmbs_subscription.fileset = run_stream_fileset_assoc.fileset
              INNER JOIN wmbs_workflow ON
                wmbs_workflow.id = wmbs_subscription.workflow AND
                wmbs_workflow.injected = 0
              INNER JOIN run_stream_style_assoc ON
                run_stream_style_assoc.run_id = run_stream_fileset_assoc.run_id AND
                run_stream_style_assoc.stream_id =   run_stream_fileset_assoc.stream_id AND
                run_stream_style_assoc.style_id = (SELECT id FROM processing_style WHERE name = 'Express')
            GROUP BY wmbs_workflow.name
          )
          """

    sqlRepackNoNotify = \
       """UPDATE wmbs_workflow
          SET injected = 1
          WHERE name in (
            SELECT wmbs_workflow.name
            FROM run_stream_fileset_assoc
              INNER JOIN wmbs_subscription ON
                wmbs_subscription.fileset = run_stream_fileset_assoc.fileset
              INNER JOIN wmbs_workflow ON
                wmbs_workflow.id = wmbs_subscription.workflow AND
                wmbs_workflow.injected = 0
              INNER JOIN run_stream_style_assoc ON
                run_stream_style_assoc.run_id = run_stream_fileset_assoc.run_id AND
                run_stream_style_assoc.stream_id =   run_stream_fileset_assoc.stream_id AND
                run_stream_style_assoc.style_id = (SELECT id FROM processing_style WHERE name = 'Bulk')
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

    def execute(self, streamerNotification, conn = None, transaction = False):

        if streamerNotification:

            self.dbi.processData(self.sqlExpressNotify, binds = {}, conn = conn,
                                 transaction = transaction)

            self.dbi.processData(self.sqlRepackNotify, binds = {}, conn = conn,
                                 transaction = transaction)

        else:

            self.dbi.processData(self.sqlExpressNoNotify, binds = {}, conn = conn,
                                 transaction = transaction)

            self.dbi.processData(self.sqlRepackNoNotify, binds = {}, conn = conn,
                                 transaction = transaction)

        return
