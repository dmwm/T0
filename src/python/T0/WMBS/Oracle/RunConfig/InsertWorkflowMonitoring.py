"""
_InsertWorkflowMonitoring_

Oracle implementation of InsertWorkflowMonitoring

Important bit is that the only unique identifier per workflow
is the top level fileset, which is the input to the first task.
Supports as input one or more fileset.ids as a list.

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertWorkflowMonitoring(DBFormatter):

    def execute(self, filesets, conn = None, transaction = False):

        sql = """INSERT INTO workflow_monitoring (WORKFLOW) 
                 VALUES ((SELECT workflow
                          FROM wmbs_subscription
                          WHERE fileset = :FILESET))
                 """

        binds = []
        for fileset in filesets: 
            binds.append( { 'FILESET' : fileset } )

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
