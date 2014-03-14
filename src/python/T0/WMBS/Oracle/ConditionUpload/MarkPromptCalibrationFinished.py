"""
_MarkPromptCalibrationFinished_

Oracle implementation of MarkPromptCalibrationFinished

Mark the PCL finished for the given run and stream.

"""

from WMCore.Database.DBFormatter import DBFormatter

class MarkPromptCalibrationFinished(DBFormatter):

    def execute(self, run, streamid, conn = None, transaction = False):

        sql = """UPDATE prompt_calib
                 SET finished = 1
                 WHERE (run_id, stream_id) IN (
                   SELECT prompt_calib.run_id, prompt_calib.stream_id
                   FROM prompt_calib
                   INNER JOIN prompt_calib_file ON
                     prompt_calib_file.run_id = prompt_calib.run_id AND
                     prompt_calib_file.stream_id = prompt_calib.stream_id
                   INNER JOIN wmbs_subscription ON
                     wmbs_subscription.id = prompt_calib_file.subscription
                   INNER JOIN wmbs_fileset ON
                     wmbs_fileset.id = wmbs_subscription.fileset
                   LEFT OUTER JOIN wmbs_sub_files_available ON
                     wmbs_sub_files_available.subscription = wmbs_subscription.id
                   LEFT OUTER JOIN wmbs_sub_files_acquired ON
                     wmbs_sub_files_acquired.subscription = wmbs_subscription.id
                   WHERE prompt_calib.run_id = :RUN
                   AND prompt_calib.stream_id = :STREAMID
                   GROUP BY prompt_calib.run_id, prompt_calib.stream_id
                   HAVING COUNT(DISTINCT wmbs_subscription.id) = MAX(prompt_calib.num_producer)
                   AND COUNT(wmbs_sub_files_available.subscription) = 0
                   AND COUNT(wmbs_sub_files_acquired.subscription) = 0
                 )
                 """

        binds = { 'RUN' : run,
                  'STREAMID' : streamid }

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
