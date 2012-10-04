"""
_MarkTrackedWorkflowMonitoring_

Oracle implementation of MarkTrackedWorkflowMonitoring.

Sets a workflow as tracked=1 in workflow_monitoring table,
should be used after successful upload to Couch.

"""

from WMCore.Database.DBFormatter import DBFormatter

class MarkTrackedWorkflowMonitoring(DBFormatter):

    def execute(self, workflowId, conn = None, transaction = False):

        sql = """UPDATE workflow_monitoring
                 SET tracked = 1
                 WHERE workflow = :WORKFLOW_ID"""

        binds = { 'WORKFLOW_ID' : workflowId }

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
