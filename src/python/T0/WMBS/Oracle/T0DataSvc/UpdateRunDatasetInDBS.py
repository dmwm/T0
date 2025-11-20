"""
_UpdateRunDatasetInDBS_

Oracle implementation of UpdateRunDatasetInDBS

Update RunDatasetDone record to mark all files as uploaded to DBS

"""

from WMCore.Database.DBFormatter import DBFormatter

class UpdateRunDatasetInDBS(DBFormatter):

    sql = """MERGE INTO run_primds_done
             USING DUAL ON ( run = :RUN AND primds = :PRIMDS )
             WHEN MATCHED THEN
               UPDATE SET in_dbs = 1
             """

    def execute(self, binds, conn = None, transaction = False):

        self.dbi.processData(self.sql, binds, conn = conn,
                             transaction = transaction)

        return