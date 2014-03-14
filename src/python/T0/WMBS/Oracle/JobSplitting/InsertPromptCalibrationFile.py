"""
_InsertPromptCalibrationFile_

Oracle implementation of InsertPromptCalibrationFile

Inserts files into the prompt_calib_file table and
marks them as acquired for the subscription. The files
will then be picked up by another piece of code,
uploaded to the DropBox and be marked as completed.

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertPromptCalibrationFile(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT ALL
                   INTO prompt_calib_file (RUN_ID, STREAM_ID, FILEID, SUBSCRIPTION)
                     VALUES (:RUN_ID, id, :FILEID, :SUBSCRIPTION)
                   INTO wmbs_sub_files_acquired (SUBSCRIPTION, FILEID)
                     VALUES (:SUBSCRIPTION, :FILEID)
                 SELECT id FROM stream
                 WHERE name = :STREAM
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        for bind in binds:
            del bind['RUN_ID']
            del bind['STREAM']

        sql = """DELETE FROM wmbs_sub_files_available
                 WHERE subscription = :SUBSCRIPTION
                 AND fileid = :FILEID"""

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
