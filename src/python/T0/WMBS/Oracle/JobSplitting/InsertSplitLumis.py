"""
_InsertSplitLumis_

Oracle implementation of InsertSplitLumis

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertSplitLumis(DBFormatter):

    sql = """INSERT INTO lumi_section_split_active
             (run_id, subscription, lumi_id, nfiles)
             SELECT run_id, :SUB, :LUMI, :NFILES
             FROM run_stream_fileset_assoc
             WHERE fileset = (SELECT fileset FROM wmbs_subscription WHERE id = :SUB)
             """

    def execute(self, binds, conn = None, transaction = False):

        self.dbi.processData(self.sql, binds, conn = conn,
                             transaction = transaction)
        return
