"""
_FinishPCLforEmptyExpress_

Oracle implementation of FinishPCLforEmptyExpress

Run/stream with data where processing of that data
completely fails will never produce conditions,
therefor set PCL to finished for these.

Second query covers the case where an Express
workflow is cleaned up before the first query
can run, also set PCL to finish for these.

"""

from WMCore.Database.DBFormatter import DBFormatter

class FinishPCLforEmptyExpress(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """UPDATE prompt_calib
                 SET finished = 1
                 WHERE (run_id, stream_id) IN (
                   SELECT prompt_calib.run_id, prompt_calib.stream_id
                   FROM prompt_calib
                   INNER JOIN run_stream_fileset_assoc ON
                     run_stream_fileset_assoc.run_id = prompt_calib.run_id AND
                     run_stream_fileset_assoc.stream_id = prompt_calib.stream_id
                   INNER JOIN wmbs_fileset ON
                     wmbs_fileset.id = run_stream_fileset_assoc.fileset AND
                     wmbs_fileset.open = 0
                   INNER JOIN wmbs_subscription ON
                     wmbs_subscription.fileset = run_stream_fileset_assoc.fileset
                   INNER JOIN wmbs_sub_files_failed ON
                     wmbs_sub_files_failed.subscription = wmbs_subscription.id
                   LEFT OUTER JOIN wmbs_sub_files_available ON
                     wmbs_sub_files_available.subscription = wmbs_subscription.id
                   LEFT OUTER JOIN wmbs_sub_files_acquired ON
                     wmbs_sub_files_acquired.subscription = wmbs_subscription.id
                   LEFT OUTER JOIN wmbs_sub_files_complete ON
                     wmbs_sub_files_complete.subscription = wmbs_subscription.id
                   WHERE checkForZeroState(prompt_calib.finished) = 0
                   AND wmbs_sub_files_available.subscription IS NULL
                   AND wmbs_sub_files_acquired.subscription IS NULL
                   AND wmbs_sub_files_complete.subscription IS NULL
                   GROUP BY prompt_calib.run_id, prompt_calib.stream_id
                 )
                 """

        results = self.dbi.processData(sql, {}, conn = conn,
                                       transaction = transaction)

        sql = """UPDATE prompt_calib
                 SET finished = 1
                 WHERE (run_id, stream_id) IN (
                   SELECT prompt_calib.run_id, prompt_calib.stream_id
                   FROM prompt_calib
                   LEFT OUTER JOIN run_stream_fileset_assoc ON
                     run_stream_fileset_assoc.run_id = prompt_calib.run_id AND
                     run_stream_fileset_assoc.stream_id = prompt_calib.stream_id
                   WHERE checkForZeroState(prompt_calib.finished) = 0
                   AND run_stream_fileset_assoc.run_id IS NULL
                 )
                 """

        results = self.dbi.processData(sql, {}, conn = conn,
                                       transaction = transaction)

        return
