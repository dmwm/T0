"""
_UpdatePromptCalibration_

Oracle implementation of UpdatePromptCalibration

Associate the PCL ConditionUpload subscription with
run and stream information, which is needed for
checking if the PCL is finished.

"""

from WMCore.Database.DBFormatter import DBFormatter

class UpdatePromptCalibration(DBFormatter):

    def execute(self, run, stream, subscription, conn = None, transaction = False):

        sql = """UPDATE prompt_calib
                 SET subscription = :SUBSCRIPTION
                 WHERE run_id = :RUN_ID
                 AND stream_id = (SELECT id FROM stream WHERE name = :STREAM)
                 """

        binds = { 'RUN_ID' : run,
                  'STREAM' : stream,
                  'SUBSCRIPTION' : subscription }

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
