"""
_GetStreamerWorkflowsForMonitoring_

Oracle implementation of ListPendingWorkflowMonitoring
Lists top level filesets not injected to monitoring
"""
from WMCore.Database.DBFormatter import DBFormatter

class GetStreamerWorkflowsForMonitoring(DBFormatter):

    def execute(self, conn = None, transaction = False):


        sql = """SELECT  wmbs_subscription.workflow, run_stream_fileset_assoc.run_id, wmbs_workflow.name
                 FROM workflow_monitoring 
                 INNER JOIN wmbs_subscription ON
                 workflow_monitoring.workflow = wmbs_subscription.workflow
                 INNER JOIN wmbs_workflow ON
                 wmbs_subscription.workflow = wmbs_workflow.id 
                 INNER JOIN run_stream_fileset_assoc ON
                 wmbs_subscription.fileset = run_stream_fileset_assoc.fileset
                 WHERE checkForZeroState(workflow_monitoring.tracked) = 0"""

        results = self.dbi.processData(sql, [], conn = conn,
                             transaction = transaction)

        return results[0].fetchall()
