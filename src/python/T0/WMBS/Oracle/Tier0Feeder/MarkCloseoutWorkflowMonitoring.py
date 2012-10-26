"""
_MarkCloseoutWorkflowMonitoring_

Oracle implementation of MarkCloseoutWorkflowMonitoring
Sets a workflow as "closeout=1" in workflow_monitoring table, should be used after successful upload to couchDB
"""
from WMCore.Database.DBFormatter import DBFormatter

class MarkCloseoutWorkflowMonitoring(DBFormatter):

    def execute(self, workflowId, conn = None, transaction = False):

        sql = """UPDATE workflow_monitoring
                 SET closeout = 1
                 WHERE workflow = :WORKFLOW_ID"""

        binds = [{'WORKFLOW_ID': workflowId}]
        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)
        return 
