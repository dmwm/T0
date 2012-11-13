"""
_GetNotClosedOutWorkflows_

Oracle implementation of GetNotClosedOutWorkflows
Lists top level filesets not injected to monitoring
"""
from WMCore.Database.DBFormatter import DBFormatter

class GetNotClosedOutWorkflows(DBFormatter):

    def execute(self, conn = None, transaction = False):


        sql = """SELECT  wmbs_subscription.workflow, wmbs_subscription.fileset, wmbs_fileset.open, wmbs_workflow.name
                 FROM workflow_monitoring 
                 INNER JOIN wmbs_subscription ON
                 workflow_monitoring.workflow = wmbs_subscription.workflow
                 INNER JOIN wmbs_workflow ON
                 wmbs_subscription.workflow = wmbs_workflow.id
                 INNER JOIN wmbs_fileset ON
                 wmbs_subscription.fileset = wmbs_fileset.id
                 WHERE checkForZeroState(workflow_monitoring.closeout) = 0"""

        results = self.dbi.processData(sql, [], conn = conn,
                             transaction = transaction)

        return results[0].fetchall()

