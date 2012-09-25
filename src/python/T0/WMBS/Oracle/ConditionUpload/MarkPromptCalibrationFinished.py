"""
_MarkPromptCalibrationFinished_

Oracle implementation of MarkPromptCalibrationFinished

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
