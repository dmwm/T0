"""
_InsertRunStreamDone_

Oracle implementation of InsertRunStreamDone

Insert RunStreamDone record

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertRunStreamDone(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO run_stream_done
                 (run_id, stream_id)
                 VALUES (:RUN,
                         (SELECT id FROM stream WHERE name = :STREAM))
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
