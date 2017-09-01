"""
_UpdateRunDatasetDone_

Oracle implementation of UpdateRunDatasetDone

Update RunDatasetDone record to PromptReco finished in Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class UpdateRunDatasetDone(DBFormatter):

    sql = """MERGE INTO run_primds_done
             USING DUAL ON ( run = :RUN AND primds = :PRIMDS )
             WHEN MATCHED THEN
               UPDATE SET finished = 1
             """

    def execute(self, binds, conn = None, transaction = False):

        self.dbi.processData(self.sql, binds, conn = conn,
                             transaction = transaction)

        return
