"""
_GetStreamerWorkflowsForMonitoring_

Oracle implementation of ListPendingWorkflowMonitoring

Lists top level filesets not injected to monitoring.

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetStreamerWorkflowsForMonitoring(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT workflow_monitoring.workflow,
                        run_stream_fileset_assoc.run_id,
                        wmbs_workflow.name
                 FROM workflow_monitoring
                   INNER JOIN wmbs_subscription ON
                     wmbs_subscription.workflow = workflow_monitoring.workflow
                   INNER JOIN run_stream_fileset_assoc ON
                     run_stream_fileset_assoc.fileset = wmbs_subscription.fileset
                   INNER JOIN wmbs_workflow ON
                     wmbs_workflow.id = workflow_monitoring.workflow
                 WHERE checkForZeroState(workflow_monitoring.tracked) = 0
                 """

        results = self.dbi.processData(sql, [], conn = conn,
                                       transaction = transaction)

        return results[0].fetchall()
