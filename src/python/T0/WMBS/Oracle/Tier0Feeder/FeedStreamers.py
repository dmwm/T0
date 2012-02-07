"""
_FeedStreamers_

Oracle implementation of FeedStreamers

For all run and stream combinations that are
configured and active (run/stream fileset is open),
check for new streamers and insert them into the
appropriate fileset. Also mark streamers as used.
Only consider streamers that are in closed lumis.

"""

import time
import logging

from WMCore.Database.DBFormatter import DBFormatter

class FeedStreamers(DBFormatter):

    def execute(self, conn = None, transaction = False):

        #
        # query only works under the assumption that there
        # is a single subscription on the run/stream fileset
        #
        sql = """INSERT ALL
                   INTO wmbs_fileset_files
                     (FILEID, FILESET, INSERT_TIME)
                     VALUES(fileid, fileset, :TIME)
                   INTO wmbs_sub_files_available
                     (SUBSCRIPTION, FILEID)
                     VALUES (subscription, fileid)
                 SELECT streamer.id AS fileid,
                        run_stream_fileset_assoc.fileset AS fileset,
                        wmbs_subscription.id AS subscription
                 FROM streamer
                 INNER JOIN run_stream_fileset_assoc ON
                   run_stream_fileset_assoc.run_id = streamer.run_id AND
                   run_stream_fileset_assoc.stream_id = streamer.stream_id
                 INNER JOIN wmbs_fileset ON
                   wmbs_fileset.id = run_stream_fileset_assoc.fileset AND
                   wmbs_fileset.open = 1
                 INNER JOIN lumi_section_closed ON
                   lumi_section_closed.run_id = streamer.run_id AND
                   lumi_section_closed.stream_id = streamer.stream_id AND
                   lumi_section_closed.lumi_id = streamer.lumi_id AND
                   lumi_section_closed.close_time > 0
                 INNER JOIN wmbs_subscription ON
                   wmbs_subscription.fileset = run_stream_fileset_assoc.fileset
                 WHERE checkForZeroState(streamer.used) = 0
                 """

        binds = { 'TIME' : int(time.time()) }
        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        #
        # streamers feed in previous query need to be updated to
        # used status, could not find a way to do it all at once
        #
        sql = """MERGE INTO streamer a
                 USING (
                   SELECT streamer.id
                   FROM streamer
                   INNER JOIN wmbs_fileset_files ON
                     wmbs_fileset_files.fileid = streamer.id
                   WHERE checkForZeroState(streamer.used) = 0
                 ) b ON ( b.id = a.id )
                 WHEN MATCHED THEN UPDATE
                   SET a.used = 1
                 """

        self.dbi.processData(sql, {}, conn = conn,
                             transaction = transaction)

        return
