"""
_InsertStreamFileset_

Oracle implementation of InsertStreamFileset

"""
import time

from WMCore.Database.DBFormatter import DBFormatter

class InsertStreamFileset(DBFormatter):

    def execute(self, run, stream, name, conn = None, transaction = False):

        sql = """INSERT ALL
                   INTO wmbs_fileset
                     (ID, NAME, LAST_UPDATE, OPEN)
                     VALUES (wmbs_fileset_SEQ.nextval, :NAME, :TIME, 1)
                   INTO run_stream_fileset_assoc
                     (RUN_ID, STREAM_ID, FILESET)
                     VALUES (:RUN, stream_id, wmbs_fileset_SEQ.nextval)
                 SELECT id AS stream_id
                 FROM stream
                 WHERE name = :STREAM
                 """

        binds = { 'RUN' : run,
                  'STREAM' : stream,
                  'NAME' : name,
                  'TIME' : int(time.time()) }

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)
        return
