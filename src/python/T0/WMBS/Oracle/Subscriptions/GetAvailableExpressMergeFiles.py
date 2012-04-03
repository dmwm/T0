"""
_GetAvailableExpressMergeFiles_

Oracle implementation of GetAvailableExpressMergeFiles

Similar to Subscriptions.GetAvailableFiles,
except also returns lumi information
"""

from WMCore.Database.DBFormatter import DBFormatter

class GetAvailableExpressMergeFiles(DBFormatter):

    def execute(self, subscription, conn = None, transaction = False):

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
                        wmbs_location.se_name AS location,
                        wmbs_fileset_files.insert_time AS insert_time
                 FROM wmbs_sub_files_available
                 INNER JOIN wmbs_file_runlumi_map ON
                   wmbs_file_runlumi_map.fileid = wmbs_sub_files_available.fileid
                 INNER JOIN wmbs_file_details ON
                   wmbs_file_details.id = wmbs_sub_files_available.fileid
                 INNER JOIN wmbs_file_location ON
                   wmbs_file_location.fileid = wmbs_sub_files_available.fileid
                 INNER JOIN wmbs_location ON
                   wmbs_location.id = wmbs_file_location.location
                 INNER JOIN wmbs_subscription ON
                   wmbs_subscription.id = wmbs_sub_files_available.subscription
                 INNER JOIN wmbs_fileset_files ON
                   wmbs_fileset_files.fileid = wmbs_sub_files_available.fileid AND
                   wmbs_fileset_files.fileset = wmbs_subscription.fileset
                 INNER JOIN wmbs_workflow_output ON
                   wmbs_workflow_output.output_fileset = wmbs_subscription.fileset
                 INNER JOIN run_stream_fileset_assoc ON
                   run_stream_fileset_assoc.run_id = wmbs_file_runlumi_map.run AND
                   run_stream_fileset_assoc.fileset =
                     ( SELECT fileset FROM wmbs_subscription WHERE workflow = wmbs_workflow_output.workflow_id )
                 LEFT OUTER JOIN lumi_section_split_active ON
                   lumi_section_split_active.run_id = wmbs_file_runlumi_map.run AND
                   lumi_section_split_active.lumi_id = wmbs_file_runlumi_map.lumi AND
                   lumi_section_split_active.stream_id = run_stream_fileset_assoc.stream_id
                 WHERE wmbs_sub_files_available.subscription = :subscription
                 AND lumi_section_split_active.run_id IS NULL
                 """

        results = self.dbi.processData(sql, { 'subscription' : subscription },
                                       conn = conn, transaction = transaction)

        return self.formatDict(results)
