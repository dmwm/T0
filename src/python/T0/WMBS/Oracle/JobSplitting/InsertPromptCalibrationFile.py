"""
_InsertPromptCalibrationFile_

Oracle implementation of InsertPromptCalibrationFile

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertPromptCalibrationFile(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT ALL
                   INTO prompt_calib_file (RUN_ID, STREAM_ID, FILEID)
                     VALUES (:RUN_ID, :STREAM_ID, :FILEID)
                   INTO wmbs_sub_files_acquired (SUBSCRIPTION, FILEID)
                     VALUES (:SUBSCRIPTION, :FILEID)
                 SELECT * FROM DUAL
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        for bind in binds:
            del bind['RUN_ID']
            del bind['STREAM_ID']

        sql = """DELETE FROM wmbs_sub_files_available
                 WHERE subscription = :SUBSCRIPTION
                 AND fileid = :FILEID"""

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
