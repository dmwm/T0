"""
_GetPromptRecoWorkflowsForMonitoring_

Oracle implementation of GetPromptRecoWorkflowsForMonitoring

Lists top level filesets not injected to monitoring which are not streamers filesets.

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetPromptRecoWorkflowsForMonitoring(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT workflow_monitoring.workflow,
                        reco_release_config.run_id,
                        wmbs_workflow.name
                 FROM workflow_monitoring
                   INNER JOIN wmbs_subscription ON
                     wmbs_subscription.workflow = workflow_monitoring.workflow
                   INNER JOIN reco_release_config ON
                     reco_release_config.fileset = wmbs_subscription.fileset
                   INNER JOIN wmbs_workflow ON
                     wmbs_workflow.id = workflow_monitoring.workflow
                 WHERE checkForZeroState(workflow_monitoring.tracked) = 0
                 """

        results = self.dbi.processData(sql, [], conn = conn,
                                       transaction = transaction)

        return results[0].fetchall()
