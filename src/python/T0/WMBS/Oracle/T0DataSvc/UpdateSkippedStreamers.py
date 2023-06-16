"""
_UpdateSkippedStreamers_

Oracle implementation of UpdateSkippedStreamers

Mark skipped streamers into T0AST

"""

from WMCore.Database.DBFormatter import DBFormatter

class UpdateSkippedStreamers(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """UPDATE streamer
                 SET skipped = 1
                 WHERE id = :ID
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
