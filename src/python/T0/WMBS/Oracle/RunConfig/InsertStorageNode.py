"""
_InsertStorageNode_

Oracle implementation of InsertStorageNode

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertStorageNode(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO storage_node
                 (NAME)
                 SELECT :NODE
                 FROM DUAL
                 WHERE NOT EXISTS (
                   SELECT * FROM storage_node
                   WHERE name = :NODE
                 )"""

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)
        return
