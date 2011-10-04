"""
_GetClosedEmptyLumis_

Oracle implementation of GetClosedEmptyLumis

For a given subscription return the closed, but
empty lumis in it's input data. Use a special
association table filled by Tier0Feeder.
"""

from WMCore.Database.DBFormatter import DBFormatter

class GetClosedEmptyLumis(DBFormatter):

    def execute(self, subscription, conn = None, transaction = False):

        sql = """SELECT lumi_section_closed.lumi AS lumi
                 FROM run_stream_sub_assoc
                 INNER JOIN lumi_section_closed ON
                   lumi_section_closed.run_id = run_stream_sub_assoc.run_id AND
                   lumi_section_closed.stream_id = run_stream_sub_assoc.stream_id AND
                   lumi_section_closed.close_time > 0 AND
                   lumi_section_closed.filecount = 0
                 WHERE run_stream_sub_assoc.subscription = :subscription
                 """

        results = self.dbi.processData(sql, { 'subscription' : subscription },
                                       conn = conn, transaction = transaction)

        lumiList = []
        for result in self.formatDict(results):
            lumiList.append(result['lumi'])

        return lumiList
