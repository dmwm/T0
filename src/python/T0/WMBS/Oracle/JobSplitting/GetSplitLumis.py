"""
_GetSplitLumis_

Oracle implementation of GetSplitLumis

Return a list of all active split lumis
Only used in job splitting unit tests
"""

from WMCore.Database.DBFormatter import DBFormatter

class GetSplitLumis(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT lumi_section_split_active.run_id,
                        lumi_section_split_active.lumi_id,
                        lumi_section_split_active.stream_id
                 FROM lumi_section_split_active
                 """

        results = self.dbi.processData(sql, conn = conn, transaction = transaction)

        return self.formatDict(results)
