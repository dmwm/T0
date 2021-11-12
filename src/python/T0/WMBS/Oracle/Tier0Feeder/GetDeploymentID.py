"""
_GetDeploymentID_

Oracle implementation of GetDeploymentID
Retrieves T0 deployment ID 
"""
from WMCore.Database.DBFormatter import DBFormatter

class GetDeploymentID(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT id
                 from t0_deployment_id"""

        results = self.dbi.processData(sql, {}, conn = conn,
                             transaction = transaction)[0].fetchall()
        id = 0
        if results:
            id=results[0][0]

        return id