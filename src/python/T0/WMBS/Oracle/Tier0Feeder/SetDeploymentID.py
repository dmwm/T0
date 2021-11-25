"""
_SetDeploymentID_

Oracle implementation of SetDeploymentID
Sets T0 deployment ID 
"""
from WMCore.Database.DBFormatter import DBFormatter

class SetDeploymentID(DBFormatter):

    def execute(self, id, conn = None, transaction = False):

        sql = """INSERT INTO t0_deployment_id
                 (name, id)
                 VALUES ('deployment_id', :ID)"""

        binds = {"ID" : id}
        results = self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
