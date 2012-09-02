"""
_InsertPromptCalibration_

Oracle implementation of InsertPromptCalibration

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertPromptCalibration(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO prompt_calib
                 (RUN_ID, STREAM_ID)
                 VALUES (:RUN,
                         (SELECT id FROM stream WHERE name = :STREAM))
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
