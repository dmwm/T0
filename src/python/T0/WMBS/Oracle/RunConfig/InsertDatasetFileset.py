"""
_InsertDatasetFileset_

Oracle implementation of InsertDatasetFileset

"""
from WMCore.Database.DBFormatter import DBFormatter

class InsertDatasetFileset(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO run_primds_fileset_assoc
                 (RUN_ID, PRIMDS_ID, FILESET)
                 VALUES (:RUN,
                         (SELECT id FROM primary_dataset WHERE name = :PRIMDS),
                         :FILESET)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)
        return
