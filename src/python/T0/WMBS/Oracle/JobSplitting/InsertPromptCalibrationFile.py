"""
_InsertPromptCalibrationFile_

Oracle implementation of InsertPromptCalibrationFile

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertPromptCalibrationFile(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT ALL
                   INTO prompt_calib_file (RUN_ID, STREAM_ID, FILEID)
                     VALUES (:RUN_ID, id, :FILEID)
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
