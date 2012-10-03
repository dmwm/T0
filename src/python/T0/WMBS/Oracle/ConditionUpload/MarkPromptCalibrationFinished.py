"""
_MarkPromptCalibrationFinished_

Oracle implementation of MarkPromptCalibrationFinished

Mark the PCL finished for the given run and stream.
There are two levels of finished here, 1 which means
the harvesting is done and 2 which means the upload
to the dropbox is complete too.

"""

from WMCore.Database.DBFormatter import DBFormatter

class MarkPromptCalibrationFinished(DBFormatter):

    def execute(self, run, stream, finished,
                conn = None, transaction = False):

        sql = """UPDATE prompt_calib
                 SET finished = :FINISHED
                 WHERE run_id = :RUN_ID
                 AND stream_id = (SELECT id FROM stream WHERE name = :STREAM)
                 """

        binds = { 'RUN_ID' : run,
                  'STREAM' : stream,
                  'FINISHED' : finished }

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
