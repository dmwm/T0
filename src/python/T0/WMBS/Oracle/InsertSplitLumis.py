"""
_InsertSplitLumis_

Oracle implementation of InsertSplitLumis

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertSplitLumis(DBFormatter):

    sql = """INSERT INTO lumi_section_split_active
             (RUN_ID, LUMI_ID, STREAM_ID)
             SELECT run_stream_sub_assoc.run_id,
                    :lumi,
                    run_stream_sub_assoc.stream_id
             FROM run_stream_sub_assoc
             WHERE run_stream_sub_assoc.subscription = :sub
             """

    def execute(self, binds, conn = None, transaction = False):

        self.dbi.processData(self.sql, binds, conn = conn,
                             transaction = transaction)
        return
