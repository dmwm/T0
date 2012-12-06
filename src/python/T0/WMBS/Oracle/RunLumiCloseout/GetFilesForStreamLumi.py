"""
_GetFilesForStreamLumi_

Oracle implementation of RunLumiCloseout.GetFilesForStreamLumi

Created on Nov 30, 2012

@author: dballest
"""

from WMCore.Database.DBFormatter import DBFormatter

class GetFilesForStreamLumi(DBFormatter):
    """
    _GetFilesForStreamLumi_

    Get the dictionary with the information
    for the files associated to the
    given run, stream and lumi.
    The dictionary keys are the files IDs (WMBS and STREAMER tables)
    and the values  are the LFNs.
    """


    sql = """SELECT wmbs_file_details.lfn,
                    streamer.id
             FROM streamer
             INNER JOIN wmbs_file_details ON
                 wmbs_file_details.id = streamer.id
             WHERE streamer.run_id = :RUN_ID AND
                   streamer.lumi_id = :LUMI_ID AND
                   streamer.stream_id = :STREAM_ID
          """

    def execute(self, run, streams, conn = None,
                transaction = False):
        """
        _execute_

        Executes the query and formats the output
        """

        binds = []
        for stream in streams:
            for lumi in streams[stream]:
                binds.append({"RUN_ID" : run,
                              "STREAM_ID" : stream,
                              "LUMI_ID" : lumi})

        result = self.dbi.processData(self.sql, binds = binds,
                                      conn = conn,
                                      transaction = transaction)

        formattedResult = self.formatDict(result)

        fileInfo = {}

        for entry in formattedResult:
            fileInfo[entry["id"]] = entry["lfn"]

        return fileInfo
