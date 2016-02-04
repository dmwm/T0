"""
_UpdateRunStreamDone_

Oracle implementation of UpdateRunStreamDone

Mark run/stream processing finished status as present in in Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class UpdateRunStreamDone(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """UPDATE run_stream_done
                 SET in_datasvc = 1
                 WHERE run_id = :RUN
                 AND stream_id = (SELECT id FROM stream WHERE name = :STREAM)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
