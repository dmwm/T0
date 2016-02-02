"""
_InsertRunStreamDone_

Oracle implementation of InsertRunStreamDone

Insert RunStreamDone record into Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertRunStreamDone(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """MERGE INTO run_stream_done
                 USING DUAL ON ( run = :RUN AND stream = :STREAM )
                 WHEN NOT MATCHED THEN
                   INSERT (run, stream)
                   VALUES (:RUN, :STREAM)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
