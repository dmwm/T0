"""
_InsertStream_

Oracle implementation of InsertStream

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertStream(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """DECLARE
                   cnt NUMBER(1);
                 BEGIN
                   SELECT COUNT(*)
                   INTO cnt
                   FROM stream
                   WHERE name = :STREAM
                   ;
                   IF (cnt = 0)
                   THEN
                     INSERT INTO stream
                     (ID, NAME)
                     VALUES(stream_SEQ.nextval, :STREAM)
                     ;
                   END IF;
                 EXCEPTION
                   WHEN DUP_VAL_ON_INDEX THEN NULL;
                 END;
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
