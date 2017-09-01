"""
_UpdateRecoLocked_

Oracle implementation of UpdateRecoLocked

Update a runs reco locked status into Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class UpdateRecoLocked(DBFormatter):

    sql = """MERGE INTO reco_locked
             USING DUAL ON ( run = :RUN )
             WHEN MATCHED THEN
               UPDATE SET locked = 1
             """

    def execute(self, binds, conn = None, transaction = False):

        self.dbi.processData(self.sql, binds, conn = conn,
                             transaction = transaction)

        return
