"""
_GetFinishedStreamers_

Oracle implementation of GetFinishedStreamers

Returns all streamer files that are completely processed (file is complete or failed).

Query works as-is since streamer files are only in a single fileset/subscription.

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetFinishedStreamers(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT streamer.id,
                        streamer.p5_id,
                        wmbs_file_details.lfn
                 FROM streamer
                 LEFT OUTER JOIN wmbs_sub_files_complete ON
                   wmbs_sub_files_complete.fileid = streamer.id
                 LEFT OUTER JOIN wmbs_sub_files_failed ON
                   wmbs_sub_files_failed.fileid = streamer.id
                 INNER JOIN wmbs_file_details ON
                   wmbs_file_details.id = streamer.id
                 WHERE checkForZeroState(streamer.deleted) = 0
                 AND ( wmbs_sub_files_complete.fileid IS NOT NULL
                       OR wmbs_sub_files_failed.fileid IS NOT NULL )
                 """

        results = self.dbi.processData(sql, {}, conn = conn,
                                       transaction = transaction)[0].fetchall()

        streamers = []
        for result in results:
            streamers.append( (result[0], result[1]) )

        return streamers
