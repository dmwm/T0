"""
_GetFinishedStreamers_

Oracle implementation of GetFinishedStreamers

Returns all streamer files that are in closed run/stream filesets
(run is over and all run/stream files are transfered/feed to Tier0)
and which are completely processed (file is not available or acquired).

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetFinishedStreamers(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT streamer.id,
                        wmbs_file_details.lfn
                 FROM streamer
                 INNER JOIN run_stream_fileset_assoc ON
                   run_stream_fileset_assoc.run_id = streamer.run_id AND
                   run_stream_fileset_assoc.stream_id = streamer.stream_id
                 INNER JOIN wmbs_fileset ON
                   wmbs_fileset.id = run_stream_fileset_assoc.fileset AND
                   wmbs_fileset.open = 0
                 LEFT OUTER JOIN wmbs_sub_files_available ON
                   wmbs_sub_files_available.fileid = streamer.id
                 LEFT OUTER JOIN wmbs_sub_files_acquired ON
                   wmbs_sub_files_acquired.fileid = streamer.id
                 INNER JOIN wmbs_file_details ON
                   wmbs_file_details.id = streamer.id
                 WHERE checkForZeroState(streamer.deleted) = 0
                 AND wmbs_sub_files_available.fileid IS NULL
                 AND wmbs_sub_files_acquired.fileid IS NULL
                 """

        results = self.dbi.processData(sql, {}, conn = conn,
                                       transaction = transaction)[0].fetchall()

        streamers = []
        for result in results:
            streamers.append( (result[0], result[1]) )

        return streamers
