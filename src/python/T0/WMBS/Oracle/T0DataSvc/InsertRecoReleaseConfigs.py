"""
_InsertRecoReleaseConfigs_

Oracle implementation of InsertRecoReleaseConfigs

Insert RecoRelease configurations into Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertRecoReleaseConfigs(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """MERGE INTO reco_locked
                 USING DUAL ON ( run = :RUN )
                 WHEN MATCHED THEN
                   UPDATE SET locked = :LOCKED
                 WHEN NOT MATCHED THEN
                   INSERT (run, locked)
                   VALUES (:RUN, :LOCKED)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
