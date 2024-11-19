"""
_GetDbsbufferBlocks_

Oracle implementation of GetDbsbufferBlocks

Returns all blocks and dbs status with their corresponding dataset and acquisition era

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetDbsbufferBlocks(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT dbsbuffer_block.blockname as block,
                        dbsbuffer_dataset.acquisition_era as acq_era,
                        dbsbuffer_block.status as status 
                 FROM dbsbuffer_block
                 INNER JOIN dbsbuffer_dataset ON dbsbuffer_dataset.id = dbsbuffer_block.dataset_id
                 WHERE checkForZeroState(dbsbuffer_block.in_datasvc) = 0
                 """

        results = self.dbi.processData(sql, binds = {}, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)
