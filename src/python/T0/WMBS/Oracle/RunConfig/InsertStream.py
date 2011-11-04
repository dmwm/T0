"""
_InsertStream_

Oracle implementation of InsertStream

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertStream(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO stream
                 (ID, NAME)
                 SELECT stream_SEQ.nextval, :STREAM
                 FROM DUAL
                 WHERE NOT EXISTS (
                   SELECT * FROM stream WHERE NAME = :STREAM
                 )"""

##         sql = """BEGIN
##                    INSERT INTO stream
##                    (ID, NAME)
##                    SELECT stream_SEQ.nextval, :STREAM
##                    FROM DUAL
##                    WHERE NOT EXISTS (
##                      SELECT * FROM stream WHERE NAME = :STREAM
##                    )
##                  EXCEPTION
##                    WHEN DUP_VAL_ON_INDEX THEN NULL;
##                    WHEN OTHERS THEN RAISE;
##                  END; 
##                  """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
