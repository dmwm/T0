"""
_InsertStreamStyle_

Oracle implementation of InsertStreamStyle

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertStreamStyle(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO run_stream_style_assoc
                 (RUN_ID, STREAM_ID, STYLE_ID)
                 VALUES (:RUN,
                         (SELECT id FROM stream WHERE name = :STREAM),
                         (SELECT id FROM processing_style WHERE name = :STYLE))
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
