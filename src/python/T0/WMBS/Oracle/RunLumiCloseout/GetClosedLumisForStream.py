"""
_GetClosedLumisForStream_

Oracle implementation of RunLumiCloseout.GetClosedLumisForStream

Created on Nov 29, 2012

@author: dballest
"""

from WMCore.Database.DBFormatter import DBFormatter

class GetClosedLumisForStream(DBFormatter):
    """
    _GetClosedLumisForStream_

    Gets the list of closed lumis for
    a given stream and run
    """

    sql = """SELECT stream_id,
                    lumi_section_closed.lumi_id,
                    (SELECT name
                     FROM stream
                     WHERE id = :STREAM_ID) AS name
             FROM lumi_section_closed
             WHERE lumi_section_closed.run_id = :RUN_ID AND
                   lumi_section_closed.stream_id = :STREAM_ID
          """


    def execute(self, run, streams, conn = None, transaction = False):
        """
        _execute_

        Returns a dictionary with the following format:

        {<streamId> : {name: <str>,
                       closedLumis: [<int>, <int>]
                      }
        }
        """

        if not streams:
            return {}
        binds = []
        for stream in streams:
            binds.append({'RUN_ID' : run,
                          'STREAM_ID' : stream})
        result = self.dbi.processData(self.sql, binds = binds,
                                      conn = conn, transaction = transaction)

        formattedResult = self.formatDict(result)
        streamInfo = {}
        for entry in formattedResult:
            if entry["stream_id"] not in streamInfo:
                streamInfo[entry["stream_id"]] = {"name" : entry["name"],
                                                  "closedLumis" : []}
            streamInfo[entry["stream_id"]]["closedLumis"].append(int(entry["lumi_id"]))

        return streamInfo
