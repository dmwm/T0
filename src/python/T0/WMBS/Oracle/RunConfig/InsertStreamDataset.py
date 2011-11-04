"""
_InsertStreamDataset_

Oracle implementation of InsertStreamDataset

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertStreamDataset(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO run_primds_stream_assoc
                 (RUN_ID, PRIMDS_ID, STREAM_ID)
                 VALUES (:RUN,
                         (SELECT id FROM primary_dataset WHERE name = :PRIMDS),
                         (SELECT id FROM stream WHERE name = :STREAM))
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
