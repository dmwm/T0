"""
_GetFileCountOnOpenLumis_

Oracle implementation of RunLumiCloseout.GetFileCountOnOpenLumis

Created on Nov 29, 2012

@author: dballest
"""

from WMCore.Database.DBFormatter import DBFormatter

class GetFileCountOnOpenLumis(DBFormatter):
    """
    GetFileCountOnOpenLumis_

    Get filecounts from lumis in the run which
    are not closed yet in lumi_section_closed
    """

    sql = """SELECT lumi_section_closed.lumi_id,
                    lumi_section_closed.stream_id,
                    stream.name,
                    lumi_section_closed.filecount AS expected_filecount,
                    COUNT(streamer.id) AS filecount
             FROM lumi_section_closed
             INNER JOIN stream ON
                 stream.id = lumi_section_closed.stream_id
             LEFT OUTER JOIN streamer ON
                 streamer.lumi_id = lumi_section_closed.lumi_id AND
                 streamer.stream_id = lumi_section_closed.stream_id AND
                 streamer.run_id = :RUN_ID
             WHERE checkForZeroState(lumi_section_closed.close_time) = 0 AND
                   lumi_section_closed.run_id = :RUN_ID
             GROUP BY lumi_section_closed.lumi_id,
                      lumi_section_closed.stream_id,
                      stream.name,
                      lumi_section_closed.filecount
             ORDER BY lumi_section_closed.lumi_id,
                      lumi_section_closed.stream_id,
                      stream.name,
                      lumi_section_closed.filecount
          """

    def execute(self, run, conn = None, transaction = False):
        """
        _execute_

        Get open lumis for a run and sort it by stream.
        """
        result = self.dbi.processData(self.sql, {"RUN_ID" : run}, conn = conn,
                                      transaction = transaction)

        formattedResult = self.formatDict(result)
        streamInfo = {}
        for entry in formattedResult:
            if (entry["stream_id"], entry["name"]) not in streamInfo:
                streamInfo[(entry["stream_id"], entry["name"])] = {}
            streamInfo[(entry["stream_id"], entry["name"])][int(entry["lumi_id"])] = (entry["expected_filecount"], entry["filecount"])

        return streamInfo
