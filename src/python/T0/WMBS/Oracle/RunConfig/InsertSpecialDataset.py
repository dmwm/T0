"""
_InsertSpecialDataset_

Oracle implementation of InsertSpecialDataset

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertSpecialDataset(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO stream_special_primds_assoc
                 (STREAM_ID, PRIMDS_ID)
                 SELECT (SELECT id FROM stream WHERE name = :STREAM),
                        (SELECT id FROM primary_dataset WHERE name = :PRIMDS)
                 FROM DUAL
                 WHERE NOT EXISTS (
                   SELECT * FROM stream_special_primds_assoc
                   WHERE stream_id = (SELECT id FROM stream WHERE name = :STREAM)
                 )
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
