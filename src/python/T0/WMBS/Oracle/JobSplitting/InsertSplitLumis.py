"""
_InsertSplitLumis_

Oracle implementation of InsertSplitLumis

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertSplitLumis(DBFormatter):

    sql = """MERGE INTO lumi_section_split_active a
             USING (
               SELECT run_id AS run_id,
                      stream_id AS stream_id,
                      :LUMI AS lumi
               FROM run_stream_fileset_assoc
               WHERE fileset =
                 (SELECT fileset FROM wmbs_subscription WHERE id = :SUB)
             ) b ON ( b.run_id = a.run_ID AND
                      b.stream_id = a.stream_id )
             WHEN NOT MATCHED THEN
               INSERT (a.run_id, a.stream_id, a.lumi_id)
               VALUES (b.run_id, b.stream_id, b.lumi)
             """

    def execute(self, binds, conn = None, transaction = False):

        self.dbi.processData(self.sql, binds, conn = conn,
                             transaction = transaction)
        return
