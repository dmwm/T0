"""
_InsertStreamer_

Oracle implementation of InsertStreamer

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertStreamer(DBFormatter):

    def execute(self, streamerPNN, binds, conn = None, transaction = False):

        sql = """DECLARE
                   cnt NUMBER(1);
                 BEGIN
                   SELECT COUNT(*)
                   INTO cnt
                   FROM wmbs_file_details
                   WHERE lfn = :LFN
                   ;
                   IF (cnt = 0)
                   THEN
                     INSERT ALL
                       INTO wmbs_file_details
                         (LFN, FILESIZE, EVENTS, MERGED)
                         VALUES (:LFN, :FILESIZE, :EVENTS, '0')
                       INTO wmbs_file_runlumi_map
                         (RUN, LUMI)
                         VALUES (:RUN, :LUMI)
                       INTO wmbs_file_location
                         (PNN)
                         VALUES ((SELECT id FROM wmbs_pnns WHERE pnn = '%s'))
                       INTO streamer
                         (P5_ID, RUN_ID, STREAM_ID, LUMI_ID, INSERT_TIME)
                         VALUES (:P5_ID, :RUN, stream_id, :LUMI, :TIME)
                     SELECT id AS stream_id
                     FROM stream
                     WHERE name = :STREAM
                     ;
                   END IF;
                 EXCEPTION
                   WHEN DUP_VAL_ON_INDEX THEN NULL;
                 END;
                 """ % streamerPNN

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
