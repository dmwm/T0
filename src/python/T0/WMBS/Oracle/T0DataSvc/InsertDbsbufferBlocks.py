"""
_InsertDbsbufferBlocks_

Oracle implementation of InsertExpressConfigs

Insert dbs blocks into Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertDbsbufferBlocks(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """MERGE INTO dbsbuffer_block
                 USING DUAL ON ( block = :BLOCK )
                 WHEN MATCHED THEN
                   UPDATE SET status = :STATUS
                 WHEN NOT MATCHED THEN
                   INSERT (block, acq_era, status)
                   VALUES (:BLOCK, :ACQ_ERA, :STATUS)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return