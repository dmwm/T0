"""
_GetAvailableRepackFiles_

Oracle implementation of GetAvailableRepackFiles

Similar to Subscriptions.GetAvailableFiles,
except also return run and lumi information
"""

from WMCore.Database.DBFormatter import DBFormatter

class GetAvailableRepackFiles(DBFormatter):

    def execute(self, subscription, conn = None, transaction = False):

        # repack input files are streamer files
        # they always have one and only one run/lumi
        # repack subscriptions are run specific
        sql = """SELECT wmbs_sub_files_available.fileid AS id,
                        wmbs_file_runlumi_map.lumi AS lumi,
                        wmbs_file_details.events AS events,
                        wmbs_file_details.filesize AS filesize,
                        wmbs_file_details.lfn AS lfn,
                        wmbs_location_senames.se_name AS location
                 FROM wmbs_sub_files_available
                 INNER JOIN run_stream_fileset_assoc ON
                   run_stream_fileset_assoc.fileset =
                     (SELECT fileset FROM wmbs_subscription WHERE id = wmbs_sub_files_available.subscription)
                 INNER JOIN wmbs_file_runlumi_map ON
                   wmbs_file_runlumi_map.fileid = wmbs_sub_files_available.fileid AND
                   wmbs_file_runlumi_map.run = run_stream_fileset_assoc.run_id
                 INNER JOIN wmbs_file_details ON
                   wmbs_file_details.id = wmbs_sub_files_available.fileid
                 INNER JOIN wmbs_file_location ON
                   wmbs_file_location.fileid = wmbs_sub_files_available.fileid
                 INNER JOIN wmbs_location ON
                   wmbs_location.id = wmbs_file_location.location
                 INNER JOIN wmbs_location_senames ON
                   wmbs_location_senames.location = wmbs_location.id
                 WHERE wmbs_sub_files_available.subscription = :subscription
                 """

        results = self.dbi.processData(sql, { 'subscription' : subscription },
                                       conn = conn, transaction = transaction)

        ungroupedResults = self.formatDict(results)
        result = {}
        for entry in ungroupedResults:
            if entry['lfn'] not in result:
                entry['location'] = set([entry['location']])
                result[entry['lfn']] = entry
            else:
                result[entry['lfn']]['location'].add(entry['location'])

        return result.values()
