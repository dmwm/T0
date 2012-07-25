"""
_GetPendingWorkflowMonitoring_

Oracle implementation of ListPendingWorkflowMonitoring
Lists top level filesets not injected to monitoring
"""
from WMCore.Database.DBFormatter import DBFormatter

class GetPendingWorkflowMonitoring(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT  wmbs_subscription.workflow, run_stream_fileset_assoc.run_id
                 FROM workflow_monitoring 
                 INNER JOIN wmbs_subscription ON
                 workflow_monitoring.fileset = wmbs_subscription.fileset
                 INNER JOIN run_stream_fileset_assoc ON
                 workflow_monitoring.fileset = run_stream_fileset_assoc.fileset
                 WHERE checkForZeroState(workflow_monitoring.tracked) = 0"""

        results = self.dbi.processData(sql, [], conn = conn,
                             transaction = transaction)
        workflows = []
        for result in results:
            if result.rowcount > 0:
                workflows.append(result.fetchall()[0])

        return workflows 
