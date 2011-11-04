"""
_InsertLumiSection_

Oracle implementation of InsertLumiSection

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertLumiSection(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO lumi_section
                 (RUN_ID, LUMI_ID)
                 SELECT :RUN,
                        :LUMI
                 FROM DUAL
                 WHERE NOT EXISTS (
                   SELECT * FROM lumi_section
                   WHERE run_id = :RUN
                   AND lumi_id = :LUMI
                 )"""

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
