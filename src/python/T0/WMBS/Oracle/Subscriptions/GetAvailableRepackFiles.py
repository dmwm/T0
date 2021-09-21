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
                        wmbs_pnns.pnn AS location,
                        wmbs_fileset_files.insert_time AS insert_time
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
                 INNER JOIN wmbs_pnns ON
                   wmbs_pnns.id = wmbs_file_location.pnn
                 INNER JOIN wmbs_subscription repack_subscription ON
                   repack_subscription.id = wmbs_sub_files_available.subscription
                 INNER JOIN wmbs_fileset_files ON
                   wmbs_fileset_files.fileid = wmbs_sub_files_available.fileid AND
                   wmbs_fileset_files.fileset = repack_subscription.fileset
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

        return list(result.values())
