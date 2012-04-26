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
                         lumi_section_split_active.subscription,
                         lumi_section_split_active.lumi_id )
                 IN (
                   SELECT lumi_section_split_active.run_id,
                          lumi_section_split_active.subscription,
                          lumi_section_split_active.lumi_id
                   FROM lumi_section_split_active
                   LEFT OUTER JOIN (
                     SELECT lumi_section_split_active.run_id,
                            wmbs_sub_files_available.subscription,
                            lumi_section_split_active.lumi_id
                     FROM wmbs_sub_files_available
                     INNER JOIN lumi_section_split_active ON
                       lumi_section_split_active.subscription = wmbs_sub_files_available.subscription
                     INNER JOIN wmbs_file_runlumi_map ON
                       wmbs_file_runlumi_map.fileid = wmbs_sub_files_available.fileid AND
                       wmbs_file_runlumi_map.run = lumi_section_split_active.run_id AND
                       wmbs_file_runlumi_map.lumi = lumi_section_split_active.lumi_id
                     UNION ALL
                     SELECT lumi_section_split_active.run_id,
                            wmbs_sub_files_acquired.subscription,
                            lumi_section_split_active.lumi_id
                     FROM wmbs_sub_files_acquired
                     INNER JOIN lumi_section_split_active ON
                       lumi_section_split_active.subscription = wmbs_sub_files_acquired.subscription
                     INNER JOIN wmbs_file_runlumi_map ON
                       wmbs_file_runlumi_map.fileid = wmbs_sub_files_acquired.fileid AND
                       wmbs_file_runlumi_map.run = lumi_section_split_active.run_id AND
                       wmbs_file_runlumi_map.lumi = lumi_section_split_active.lumi_id
                     UNION ALL
                     SELECT lumi_section_split_active.run_id,
                            wmbs_sub_files_failed.subscription,
                            lumi_section_split_active.lumi_id
                     FROM wmbs_sub_files_failed
                     INNER JOIN lumi_section_split_active ON
                       lumi_section_split_active.subscription = wmbs_sub_files_failed.subscription
                     INNER JOIN wmbs_file_runlumi_map ON
                       wmbs_file_runlumi_map.fileid = wmbs_sub_files_failed.fileid AND
                       wmbs_file_runlumi_map.run = lumi_section_split_active.run_id AND
                       wmbs_file_runlumi_map.lumi = lumi_section_split_active.lumi_id
                   ) incomplete_files ON
                     incomplete_files.run_id = lumi_section_split_active.run_id AND
                     incomplete_files.subscription = lumi_section_split_active.subscription AND
                     incomplete_files.lumi_id = lumi_section_split_active.lumi_id
                   GROUP BY lumi_section_split_active.run_id,
                            lumi_section_split_active.subscription,
                            lumi_section_split_active.lumi_id
                   HAVING COUNT(incomplete_files.run_id) = 0
                 )
                 """

        self.dbi.processData(sql, binds = {}, conn = conn,
                             transaction = transaction)

        return
