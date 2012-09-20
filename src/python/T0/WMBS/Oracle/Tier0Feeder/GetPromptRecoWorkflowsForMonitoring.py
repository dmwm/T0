"""
_GetPromptRecoWorkflowsForMonitoring_

Oracle implementation of GetPromptRecoWorkflowsForMonitoring
Lists top level filesets not injected to monitoring which are not streamers filesets
"""
from WMCore.Database.DBFormatter import DBFormatter

class GetPromptRecoWorkflowsForMonitoring(DBFormatter):

    def execute(self, conn = None, transaction = False):
        sql = """SELECT  wmbs_subscription.workflow, reco_release_config.run_id, wmbs_workflow.name
                 FROM workflow_monitoring 
                 INNER JOIN wmbs_subscription ON
                 workflow_monitoring.workflow = wmbs_subscription.workflow
                 INNER JOIN wmbs_workflow ON
                 wmbs_subscription.workflow = wmbs_workflow.id 
                 INNER JOIN reco_release_config ON
                 wmbs_subscription.fileset = reco_release_config.fileset
                 WHERE checkForZeroState(workflow_monitoring.tracked) = 0"""

        results = self.dbi.processData(sql, [], conn = conn,
                             transaction = transaction)

        return results[0].fetchall()
