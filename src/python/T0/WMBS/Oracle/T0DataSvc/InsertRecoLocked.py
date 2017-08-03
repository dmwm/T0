"""
_InsertRecoLocked_

Oracle implementation of InsertRecoLocked

Insert a runs reco locked status into Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertRecoLocked(DBFormatter):

    sql = """MERGE INTO reco_locked
             USING DUAL ON ( run = :RUN )
             WHEN NOT MATCHED THEN
               INSERT (run, locked)
               VALUES (:RUN, 0)
             """

    def execute(self, binds, conn = None, transaction = False):

        self.dbi.processData(self.sql, binds, conn = conn,
                             transaction = transaction)

        return
