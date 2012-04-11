"""
_CheckActiveSplitLumis_

Oracle implementation of CheckActiveSplitLumis



"""
import time

from WMCore.Database.DBFormatter import DBFormatter

class CheckActiveSplitLumis(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """DELETE FROM lumi_section_split_active
                 WHERE ( lumi_section_split_active.run_id,
                         lumi_section_split_active.lumi_id,
                         lumi_section_split_active.stream_id )
                 IN (
                   SELECT lumi_section_split_active.run_id,
                          lumi_section_split_active.lumi_id,
                          lumi_section_split_active.stream_id
                   FROM lumi_section_split_active
                   INNER JOIN streamer ON
                     streamer.run_id = lumi_section_split_active.run_id AND
                     streamer.lumi_id = lumi_section_split_active.lumi_id AND
                     streamer.stream_id = lumi_section_split_active.stream_id
                   LEFT OUTER JOIN (
                     SELECT * FROM wmbs_sub_files_available
                     UNION ALL
                     SELECT * FROM wmbs_sub_files_acquired
                     UNION ALL
                     SELECT * FROM wmbs_sub_files_failed
                   ) incomplete_files ON
                     incomplete_files.fileid = streamer.id
                   GROUP BY lumi_section_split_active.run_id,
                            lumi_section_split_active.lumi_id,
                            lumi_section_split_active.stream_id
                   HAVING COUNT(incomplete_files.fileid) = 0
                 )
                 """

        self.dbi.processData(sql, binds = {}, conn = conn,
                             transaction = transaction)

        return
