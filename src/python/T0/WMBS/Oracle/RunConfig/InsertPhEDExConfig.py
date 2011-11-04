"""
_InsertPhEDExConfig_

Oracle implementation of InsertPhEDExConfig

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertPhEDExConfig(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO phedex_config
                 (RUN_ID, PRIMDS_ID, NODE_ID, CUSTODIAL, REQUEST_ONLY, PRIORITY)
                 VALUES (:run,
                         (SELECT id FROM primary_dataset WHERE name = :PRIMDS),
                         (SELECT id FROM storage_node WHERE name = :NODE),
                         :CUSTODIAL,
                         :REQ_ONLY,
                         :PRIO)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)
        return
