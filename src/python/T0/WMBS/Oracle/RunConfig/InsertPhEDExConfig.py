"""
_InsertPhEDExConfig_

Oracle implementation of InsertPhEDExConfig

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertPhEDExConfig(DBFormatter):

    sql = """INSERT INTO phedex_config
             (RUN_ID, PRIMDS_ID, ARCHIVAL_NODE_ID, TAPE_NODE_ID, DISK_NODE_ID, DISK_NODE_RECO_ID)
             VALUES (:RUN,
                    (SELECT id FROM primary_dataset WHERE name = :PRIMDS),
                    (SELECT id FROM storage_node WHERE name = :ARCHIVAL_NODE),
                    (SELECT id FROM storage_node WHERE name = :TAPE_NODE),
                    (SELECT id FROM storage_node WHERE name = :DISK_NODE),
                    (SELECT id FROM storage_node WHERE name = :DISK_NODE_RECO))
             """

    def execute(self, binds, conn = None, transaction = False):

        self.dbi.processData(self.sql, binds, conn = conn,
                             transaction = transaction)

        return
