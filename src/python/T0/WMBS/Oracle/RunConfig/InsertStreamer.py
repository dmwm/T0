"""
_InsertStreamer_

Oracle implementation of InsertStreamer

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertStreamer(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT ALL
                   INTO wmbs_file_details
                     (ID, LFN, FILESIZE, EVENTS, MERGED)
                     VALUES (wmbs_file_details_SEQ.nextval, :LFN, :FILESIZE, :EVENTS, '1')
                   INTO wmbs_file_runlumi_map
                     (FILEID, RUN, LUMI)
                     VALUES (wmbs_file_details_SEQ.nextval, :RUN, :LUMI)
                   INTO streamer
                     (ID, RUN_ID, STREAM_ID, LUMI_ID, INSERT_TIME)
                     VALUES (wmbs_file_details_SEQ.nextval, :RUN, stream_id, :LUMI, :TIME)
                 SELECT id AS stream_id
                 FROM stream
                 WHERE name = :STREAM
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
