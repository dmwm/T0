"""
_GetAvailableConditionFiles_

Oracle implementation of GetAvailableConditionFiles

Similar to Subscriptions.GetAvailableFiles, 
except it only returns file ids, nothing else
"""

from WMCore.Database.DBFormatter import DBFormatter

class GetAvailableConditionFiles(DBFormatter):

    def execute(self, subscription, conn = None, transaction = False):

        sql = """SELECT wmbs_sub_files_available.fileid AS id
                 FROM wmbs_sub_files_available
                 WHERE wmbs_sub_files_available.subscription = :subscription
                 """

        results = self.dbi.processData(sql, { 'subscription' : subscription },
                                       conn = conn, transaction = transaction)

        return self.formatDict(results)
