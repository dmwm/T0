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
                         (ID, LFN, FILESIZE, EVENTS, MERGED)
                         VALUES (wmbs_file_details_SEQ.nextval, :LFN, :FILESIZE, :EVENTS, '0')
                       INTO wmbs_file_runlumi_map
                         (FILEID, RUN, LUMI)
                         VALUES (wmbs_file_details_SEQ.nextval, :RUN, :LUMI)
                       INTO wmbs_file_location
                         (FILEID, PNN)
                         VALUES (wmbs_file_details_SEQ.nextval, (SELECT id FROM wmbs_pnns WHERE pnn = '%s'))
                       INTO streamer
                         (ID, P5_ID, RUN_ID, STREAM_ID, LUMI_ID, INSERT_TIME)
                         VALUES (wmbs_file_details_SEQ.nextval, :P5_ID, :RUN, stream_id, :LUMI, :TIME)
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
