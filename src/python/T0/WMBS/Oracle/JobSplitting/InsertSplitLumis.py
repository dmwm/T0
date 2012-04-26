"""
_InsertSplitLumis_

Oracle implementation of InsertSplitLumis

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertSplitLumis(DBFormatter):

    sql = """MERGE INTO lumi_section_split_active a
             USING (
               SELECT run_id AS run_id,
                      :SUB AS subscription,
                      :LUMI AS lumi_id
               FROM run_stream_fileset_assoc
               WHERE fileset =
                 (SELECT fileset FROM wmbs_subscription WHERE id = :SUB)
             ) b ON ( b.run_id = a.run_id AND
                      b.subscription = a.subscription )
             WHEN NOT MATCHED THEN
               INSERT (run_id, subscription, lumi_id)
               VALUES (b.run_id, b.subscription, b.lumi_id)
             """

    def execute(self, binds, conn = None, transaction = False):

        self.dbi.processData(self.sql, binds, conn = conn,
                             transaction = transaction)
        return
