"""
_InsertStreamer_

Oracle implementation of InsertStreamer

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertStreamer(DBFormatter):

    def execute(self, streamerPNN, binds, conn = None, transaction = False):

        sql = """DECLARE
                   cnt NUMBER(1);
                   file_id NUMBER;
                   stream_id NUMBER;
                 BEGIN
                   SELECT COUNT(*)
                   INTO cnt
                   FROM wmbs_file_details
                   WHERE lfn = :LFN
                   ;

                   SELECT id INTO stream_id
                   FROM stream
                   WHERE name = :STREAM;

                   IF (cnt = 0)
                   THEN
                     INSERT INTO wmbs_file_details
                       (LFN, FILESIZE, EVENTS, MERGED)
                       VALUES (:LFN, :FILESIZE, :EVENTS, '0')
                       RETURNING id INTO file_id;

                     INSERT INTO wmbs_file_runlumi_map
                       (FILEID, RUN, LUMI)
                       VALUES (file_id, :RUN, :LUMI);

                     INSERT INTO wmbs_file_location
                       (FILEID, PNN)
                       VALUES (file_id, (SELECT id FROM wmbs_pnns WHERE pnn = '%s'));

                     INSERT INTO streamer
                       (ID, P5_ID, RUN_ID, STREAM_ID, LUMI_ID, INSERT_TIME)
                       VALUES (file_id, :P5_ID, :RUN, stream_id, :LUMI, :TIME);
                   END IF;
                 EXCEPTION
                   WHEN DUP_VAL_ON_INDEX THEN NULL;
                 END;
                 """ % streamerPNN

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
