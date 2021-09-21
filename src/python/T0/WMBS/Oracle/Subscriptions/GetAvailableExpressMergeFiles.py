"""
_GetAvailableExpressMergeFiles_

Oracle implementation of GetAvailableExpressMergeFiles

Similar to Subscriptions.GetAvailableFiles,
except also returns lumi information
"""

from WMCore.Database.DBFormatter import DBFormatter

class GetAvailableExpressMergeFiles(DBFormatter):

    def execute(self, subscription, conn = None, transaction = False):

        #
        # express merge input files always have one and
        # only one run/lumi (it's how they are produced)
        #
        # ignore files that are from active split lumis
        #
        # expressmerge subscriptions are run specific
        #

        sql = """SELECT wmbs_sub_files_available.fileid AS id,
                        wmbs_file_runlumi_map.lumi AS lumi,
                        wmbs_file_details.filesize AS filesize,
                        wmbs_file_details.lfn AS lfn,
                        wmbs_pnns.pnn AS location,
                        wmbs_fileset_files.insert_time AS insert_time
                 FROM wmbs_sub_files_available
                 INNER JOIN wmbs_file_runlumi_map ON
                   wmbs_file_runlumi_map.fileid = wmbs_sub_files_available.fileid
                 INNER JOIN wmbs_file_details ON
                   wmbs_file_details.id = wmbs_sub_files_available.fileid
                 INNER JOIN wmbs_file_location ON
                   wmbs_file_location.fileid = wmbs_sub_files_available.fileid
                 INNER JOIN wmbs_pnns ON
                   wmbs_pnns.id = wmbs_file_location.pnn
                 INNER JOIN wmbs_subscription expressmerge_subscription ON
                   expressmerge_subscription.id = wmbs_sub_files_available.subscription
                 INNER JOIN wmbs_fileset_files ON
                   wmbs_fileset_files.fileid = wmbs_sub_files_available.fileid AND
                   wmbs_fileset_files.fileset = expressmerge_subscription.fileset
                 INNER JOIN wmbs_workflow_output ON
                   wmbs_workflow_output.output_fileset = expressmerge_subscription.fileset
                 INNER JOIN wmbs_subscription express_subscription ON
                   express_subscription.workflow = wmbs_workflow_output.workflow_id
                 LEFT OUTER JOIN lumi_section_split_active ON
                   lumi_section_split_active.run_id = wmbs_file_runlumi_map.run AND
                   lumi_section_split_active.lumi_id = wmbs_file_runlumi_map.lumi AND
                   lumi_section_split_active.subscription = express_subscription.id
                 WHERE wmbs_sub_files_available.subscription = :subscription
                 AND lumi_section_split_active.run_id IS NULL
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
