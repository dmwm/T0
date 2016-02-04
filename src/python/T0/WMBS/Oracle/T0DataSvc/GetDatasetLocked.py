"""
_GetDatasetLocked_

Oracle implementation of GetDatasetLocked

Returns datasets which are not yet locked

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetDatasetLocked(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT dbsbuffer_dataset.id AS id,
                        dbsbuffer_dataset.path AS path
                 FROM dbsbuffer_dataset
                 LEFT OUTER JOIN dataset_locked ON
                   dataset_locked.dataset_id = dbsbuffer_dataset.id
                 WHERE dataset_locked.dataset_id IS NULL
                 """

        results = self.dbi.processData(sql, binds = {}, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)
