"""
_InsertLumiSection_

Oracle implementation of InsertLumiSection

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertLumiSection(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """DECLARE
                   cnt NUMBER(1);
                 BEGIN
                   SELECT COUNT(*)
                   INTO cnt
                   FROM lumi_section
                   WHERE run_id = :RUN
                   AND lumi_id = :LUMI
                   ;
                   IF (cnt = 0)
                   THEN
                     INSERT INTO lumi_section
                     (RUN_ID, LUMI_ID)
                     VALUES(:RUN, :LUMI)
                     ;
                   END IF;
                 EXCEPTION
                   WHEN DUP_VAL_ON_INDEX THEN NULL;
                 END;
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
