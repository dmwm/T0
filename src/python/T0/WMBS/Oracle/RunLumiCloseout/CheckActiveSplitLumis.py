"""
_CheckActiveSplitLumis_

Oracle implementation of CheckActiveSplitLumis

Check active split lumis for completetion and delete if complete.

An active split lumi is complete if the number of complete
file records is equal to the total numbers of streamer files
in that lumi.

"""
import time

from WMCore.Database.DBFormatter import DBFormatter

class CheckActiveSplitLumis(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """DELETE FROM lumi_section_split_active
                 WHERE ( lumi_section_split_active.subscription,
                         lumi_section_split_active.run_id,
                         lumi_section_split_active.lumi_id )
                 IN (
                   SELECT lumi_section_split_active.subscription,
                          lumi_section_split_active.run_id,
                          lumi_section_split_active.lumi_id
                   FROM lumi_section_split_active
                   INNER JOIN wmbs_sub_files_complete ON
                     wmbs_sub_files_complete.subscription = lumi_section_split_active.subscription
                   INNER JOIN wmbs_file_runlumi_map ON
                     wmbs_file_runlumi_map.fileid = wmbs_sub_files_complete.fileid AND
                     wmbs_file_runlumi_map.run = lumi_section_split_active.run_id AND
                     wmbs_file_runlumi_map.lumi = lumi_section_split_active.lumi_id
                   GROUP BY lumi_section_split_active.subscription,
                            lumi_section_split_active.run_id,
                            lumi_section_split_active.lumi_id
                   HAVING COUNT(*) = MAX(lumi_section_split_active.nfiles)
                 )
                 """

        self.dbi.processData(sql, binds = {}, conn = conn,
                             transaction = transaction)

        return
