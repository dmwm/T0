"""
_InsertSkippedStreamers_

Oracle implementation of InsertSkippedStreamers

Insert skipped streamers into Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertSkippedStreamers(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """MERGE INTO skipped_streamers
                 USING DUAL ON ( run = :RUN AND stream = :STREAM and lumi = :LUMI )
                 WHEN NOT MATCHED THEN
                   INSERT (run, stream, lumi, events)
                   VALUES (:RUN, :STREAM, :LUMI, :EVENTS)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
