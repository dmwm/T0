"""
_InsertErrorDataset_

Oracle implementation of InsertErrorDataset

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertErrorDataset(DBFormatter):

    sql = """INSERT INTO primds_error_primds_assoc
             (PARENT_ID, ERROR_ID)
             SELECT (SELECT id FROM primary_dataset WHERE name = :PARENT),
                    (SELECT id FROM primary_dataset WHERE name = :ERROR)
             FROM DUAL
             WHERE NOT EXISTS (
               SELECT * FROM primds_error_primds_assoc
               WHERE parent_id = (SELECT id FROM primary_dataset WHERE name = :PARENT)
             )"""

    def execute(self, binds, conn = None, transaction = False):

        self.dbi.processData(self.sql, binds, conn = conn,
                             transaction = transaction)
        return
