"""
_CheckClosedLumis_

Oracle implementation of RunLumiCloseout.CheckClosedLumis

Created on Nov 29, 2012

@author: dballest
"""

from WMCore.Database.DBFormatter import DBFormatter

class CheckClosedLumis(DBFormatter):
    """
    _CheckClosedLumis_

    Cross-checks the number of closed lumis for
    every stream in a run with the lumicount
    in the run table
    """

    sql = """SELECT stream_id,
                    COUNT(*) AS closed_lumi_count,
                    MAX(lumi_id) AS max_lumi,
                    (SELECT lumicount
                     FROM run
                     WHERE run_id = :RUN_ID) AS expected_lumi_count
             FROM lumi_section_closed
             WHERE run_id = :RUN_ID
             GROUP BY stream_id
          """

    def execute(self, run, conn = None, transaction = False):
        """
        _execute_

        Basic execute query plus formatDict
        """
        result = self.dbi.processData(self.sql, {'RUN_ID': run}, conn = conn,
                                      transaction = transaction)

        return self.formatDict(result)
