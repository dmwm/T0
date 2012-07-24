"""
_MarkTrackedWorkflowMonitoring_

Oracle implementation of MarkTrackedWorkflowMonitoring
Sets a workflow as "tracked=1" in workflow_monitoring table, should be used after successful upload to couchDB
"""
from WMCore.Database.DBFormatter import DBFormatter

class MarkTrackedWorkflowMonitoring(DBFormatter):

    def execute(self, workflowId, conn = None, transaction = False):

        sql = """UPDATE workflow_monitoring
                 SET tracked = 1
                 WHERE fileset = (
                     SELECT  workflow_monitoring.fileset
                     FROM workflow_monitoring 
                     INNER JOIN wmbs_subscription ON
                     workflow_monitoring.fileset = wmbs_subscription.fileset
                     INNER JOIN run_stream_fileset_assoc ON
                     workflow_monitoring.fileset = run_stream_fileset_assoc.fileset
                     WHERE wmbs_subscription.workflow = :WORKFLOW_ID
                 )"""

        binds = [{'WORKFLOW_ID': workflowId}]
        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)
        return 
