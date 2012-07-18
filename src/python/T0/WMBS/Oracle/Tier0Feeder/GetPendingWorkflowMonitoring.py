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
                 WHERE workflow_monitoring.tracked = 0"""

        binds = []
        #for filesetId in filesetIds : 
        #    binds.append({'FILESET_ID': filesetId})

        result = self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)
        workflows = []
        for row in result:
            (workflow, run) = row.data[0]
            workflows.append({"workflow" : workflow,
                                "run" : run})
            
        return workflows


# top level Fileset ID, then TOP LEVEL SUBSCRIPTION ID
# run number

