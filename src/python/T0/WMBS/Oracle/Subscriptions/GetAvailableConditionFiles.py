"""
_GetAvailableConditionFiles_

Oracle implementation of GetAvailableRepackFiles

Similar to Subscriptions.GetAvailableFiles, 
except it only returns file ids, nothing else
"""

from WMCore.Database.DBFormatter import DBFormatter

class GetAvailableConditionFiles(DBFormatter):

    def execute(self, subscription, conn = None, transaction = False):

        sql = """SELECT wmbs_sub_files_available.fileid AS id,
                        streamer.run_id AS run_id,
                        streamer.stream_id AS stream_id
                 FROM wmbs_sub_files_available
                 INNER JOIN wmbs_file_parent a ON
                   a.child = wmbs_sub_files_available.fileid
                 INNER JOIN wmbs_file_parent b ON
                   b.child = a.parent
                 INNER JOIN wmbs_file_parent c ON
                   c.child = b.parent
                 INNER JOIN streamer ON
                   streamer.id = c.parent
                 WHERE wmbs_sub_files_available.subscription = :subscription
                 GROUP BY wmbs_sub_files_available.fileid,
                          streamer.run_id,
                          streamer.stream_id
                 """

        results = self.dbi.processData(sql, { 'subscription' : subscription },
                                       conn = conn, transaction = transaction)

        return self.formatDict(results)
