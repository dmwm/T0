"""
_InsertPrimaryDataset_

Oracle implementation of InsertPrimaryDataset

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertPrimaryDataset(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO primary_dataset
                 (ID, NAME)
                 SELECT primary_dataset_SEQ.nextval, :PRIMDS
                 FROM DUAL
                 WHERE NOT EXISTS (
                   SELECT * FROM primary_dataset
                   WHERE NAME = :PRIMDS
                 )"""

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
