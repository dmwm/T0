"""
_GetClosedEmptyLumis_

Oracle implementation of GetClosedEmptyLumis

For a given subscription return the closed, but
empty lumis in it's input data. Use a special
association table filled by Tier0Feeder.
"""

from WMCore.Database.DBFormatter import DBFormatter

class GetClosedEmptyLumis(DBFormatter):

    sql = """SELECT lumi_section_closed.lumi_id
             FROM run_stream_fileset_assoc
             INNER JOIN lumi_section_closed ON
               lumi_section_closed.run_id = run_stream_fileset_assoc.run_id AND
               lumi_section_closed.stream_id = run_stream_fileset_assoc.stream_id AND
               lumi_section_closed.close_time > 0 AND
               lumi_section_closed.filecount = 0
             WHERE run_stream_fileset_assoc.fileset =
               (SELECT fileset FROM wmbs_subscription WHERE id = :subscription)
             """

    def execute(self, subscription, conn = None, transaction = False):

        results = self.dbi.processData(self.sql, { 'subscription' : subscription },
                                       conn = conn, transaction = transaction)[0].fetchall()

        lumiList = []
        for result in results:
            lumiList.append(result[0])

        return lumiList
