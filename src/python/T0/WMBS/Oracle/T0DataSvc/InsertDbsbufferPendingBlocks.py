"""
_InsertDbsbufferPendingBlocks_

Oracle implementation of InsertDbsbufferPendingBlocks

Insert count of pending blocks by era into Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertDbsbufferPendingBlocks(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """MERGE INTO dbsbuffer_pending_blocks
                 USING DUAL ON ( acq_era = :ACQ_ERA )
                 WHEN MATCHED THEN
                   UPDATE SET pending_blocks = :PENDING_BLOCKS
                 WHEN NOT MATCHED THEN
                   INSERT (acq_era, pending_blocks)
                   VALUES (:ACQ_ERA, :PENDING_BLOCKS)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return