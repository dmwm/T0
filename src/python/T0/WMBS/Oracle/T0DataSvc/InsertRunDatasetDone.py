"""
_InsertRunDatasetDone_

Oracle implementation of InsertRunDatasetDone

Insert RunDatasetDone record into Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertRunDatasetDone(DBFormatter):

    sql = """MERGE INTO run_primds_done
             USING DUAL ON ( run = :RUN AND primds = :PRIMDS )
             WHEN NOT MATCHED THEN
               INSERT (run, primds)
               VALUES (:RUN, :PRIMDS)
             """

    def execute(self, binds, conn = None, transaction = False):

        self.dbi.processData(self.sql, binds, conn = conn,
                             transaction = transaction)

        return
