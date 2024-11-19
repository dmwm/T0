"""
_GetDbsbufferPendingBlocks_

Oracle implementation of GetDbsbufferPendingBlocks

Returns count of dbs blocks with status different than InDBS by acquisition era

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetDbsbufferPendingBlocks(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT dbsbuffer_dataset.acquisition_era as acq_era, COUNT(dbsbuffer_block.blockname) as pending_blocks
                 FROM dbsbuffer_block
                 INNER JOIN dbsbuffer_dataset ON dbsbuffer_dataset.id = dbsbuffer_block.dataset_id
                 WHERE dbsbuffer_block.status NOT LIKE 'InDBS'
                 """

        results = self.dbi.processData(sql, binds = {}, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)
