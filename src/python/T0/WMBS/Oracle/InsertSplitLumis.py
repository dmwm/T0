"""
_InsertSplitLumis_

Oracle implementation of InsertSplitLumis

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertSplitLumis(DBFormatter):

    sql = """BEGIN
               INSERT INTO lumi_section_split_active
               (RUN_ID, LUMI_ID, STREAM_ID)
               VALUES (:run_id, :lumi_id, :stream_id);
             EXCEPTION
               WHEN DUP_VAL_ON_INDEX THEN NULL;
               WHEN OTHERS THEN RAISE;
             END;
             """

    def execute(self, binds, conn = None, transaction = False):

        self.dbi.processData(self.sql, binds, conn = conn,
                             transaction = transaction)
        return
