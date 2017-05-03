"""
_InsertOfflineFileStatus_

Oracle implementation of InsertOfflineFileStatus

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertOfflineFileStatus(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """DECLARE
                   cnt NUMBER(1);
                 BEGIN
                   SELECT COUNT(*)
                   INTO cnt
                   FROM file_transfer_status_offline
                   WHERE p5_fileid = :P5_ID
                   ;
                   IF (cnt = 0)
                   THEN
                     INSERT INTO file_transfer_status_offline
                     (P5_FILEID, FILENAME, T0_CHECKED_TIME, CHECKED_RETRIEVE)
                     VALUES(:P5_ID, :FILENAME, CURRENT_TIMESTAMP, 1)
                     ;
                   END IF;
                 EXCEPTION
                   WHEN DUP_VAL_ON_INDEX THEN NULL;
                 END;
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
