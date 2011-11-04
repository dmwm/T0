"""
_InsertStorageNode_

Oracle implementation of InsertStorageNode

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertStorageNode(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO storage_node
                 (ID, NAME)
                 SELECT storage_node_SEQ.nextval, :NODE
                 FROM DUAL
                 WHERE NOT EXISTS (
                   SELECT * FROM storage_node
                   WHERE name = :NODE
                 )"""

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)
        return
