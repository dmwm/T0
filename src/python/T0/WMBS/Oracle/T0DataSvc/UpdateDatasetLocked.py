"""
_UpdateDatasetLocked_

Oracle implementation of UpdateDatasetLocked

Mark datasets as present/locked in Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class UpdateDatasetLocked(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO dataset_locked
                 (dataset_id)
                 VALUES (:ID)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
