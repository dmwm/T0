"""
_InsertDatasetLocked_

Oracle implementation of InsertDatasetLocked

Insert locked datasets into Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertDatasetLocked(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """MERGE INTO dataset_locked
                 USING DUAL ON ( path = :PATH )
                 WHEN NOT MATCHED THEN
                   INSERT (path)
                   VALUES (:PATH)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
