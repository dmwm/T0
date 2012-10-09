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
                 WHERE run_id = :RUN
                 AND stream_id = :STREAMID
                 """

        binds = { 'RUN' : run,
                  'STREAMID' : streamid }

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
