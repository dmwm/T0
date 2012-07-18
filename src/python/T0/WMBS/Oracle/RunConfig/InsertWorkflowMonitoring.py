"""
_InsertWorkflowMonitoring_

Oracle implementation of InsertWorkflowMonitoring
Important bit is that the only unique identifier per worklfow, is the top level fileset, which is the input to the first task.
Supports as input one or more fileset.id's as a [list]
"""
from WMCore.Database.DBFormatter import DBFormatter

class InsertWorkflowMonitoring(DBFormatter):

    def execute(self, filesetIds, conn = None, transaction = False):

        sql = """INSERT INTO workflow_monitoring 
                (id) 
                VALUES ((SELECT wmbs_subscription.workflow FROM wmbs_subscription WHERE wmbs_subscription.fileset = :FILESET_ID))"""

        binds = []
        for filesetId in filesetIds : 
            binds.append({'FILESET_ID': filesetId})

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)
        return
