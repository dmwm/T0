"""
_InsertRecoReleaseConfig_

Oracle implementation of InsertRecoReleaseConfig

"""
from WMCore.Database.DBFormatter import DBFormatter

class InsertRecoReleaseConfig(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO reco_release_config
                 (RUN_ID, PRIMDS_ID, FILESET, DELAY, DELAY_OFFSET)
                 VALUES (:RUN,
                         (SELECT id FROM primary_dataset WHERE name = :PRIMDS),
                         :FILESET,
                         0,
                         0)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)
        return
