"""
_GetAvailableExpressFiles_

Oracle implementation of GetAvailableExpressFiles

Similar to Subscriptions.GetAvailableFiles,
except also return run and lumi information
"""

from WMCore.Database.DBFormatter import DBFormatter

class GetAvailableExpressFiles(DBFormatter):

    def execute(self, subscription, conn = None, transaction = False):

        # express input files are streamer files
        # they always have one and only one run/lumi
        # express subscriptions are run specific
        sql = """SELECT wmbs_sub_files_available.fileid AS id,
                        wmbs_file_runlumi_map.lumi AS lumi,
                        wmbs_file_details.events AS events,
                        wmbs_location.se_name AS location
                 FROM wmbs_sub_files_available
                 INNER JOIN wmbs_file_runlumi_map ON
                   wmbs_file_runlumi_map.fileid = wmbs_sub_files_available.fileid
                 INNER JOIN wmbs_file_details ON
                   wmbs_file_details.id = wmbs_sub_files_available.fileid
                 INNER JOIN wmbs_file_location ON
                   wmbs_file_location.fileid = wmbs_sub_files_available.fileid
                 INNER JOIN wmbs_location ON
                   wmbs_location.id = wmbs_file_location.location
                 WHERE wmbs_sub_files_available.subscription = :subscription
                 """

        results = self.dbi.processData(sql, { 'subscription' : subscription },
                                       conn = conn, transaction = transaction)

        return self.formatDict(results)
