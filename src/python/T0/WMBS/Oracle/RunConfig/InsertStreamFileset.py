"""
_InsertStreamFileset_

Oracle implementation of InsertStreamFileset

"""
import time

from WMCore.Database.DBFormatter import DBFormatter

class InsertStreamFileset(DBFormatter):

    def execute(self, run, stream, name, conn = None, transaction = False):

        sql = """DECLARE
                   fileset_id NUMBER;
                   stream_id NUMBER;
                 BEGIN
                   SELECT id INTO stream_id
                   FROM stream
                   WHERE name = :STREAM;

                   INSERT INTO wmbs_fileset
                     (NAME, LAST_UPDATE, OPEN)
                     VALUES (:NAME, :TIME, 1)
                     RETURNING id INTO fileset_id;

                   INSERT INTO run_stream_fileset_assoc
                     (RUN_ID, STREAM_ID, FILESET)
                     VALUES (:RUN, stream_id, fileset_id);
                 END;
                 """

        binds = { 'RUN' : run,
                  'STREAM' : stream,
                  'NAME' : name,
                  'TIME' : int(time.time()) }

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)
        return
