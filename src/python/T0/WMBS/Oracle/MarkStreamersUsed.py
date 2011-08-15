"""
_MarkStreamersUsed_

Oracle implementation of MarkStreamersUsed

"""

from WMCore.Database.DBFormatter import DBFormatter

class MarkStreamersUsed(DBFormatter):

    sql = """UPDATE streamer SET used = 1
             WHERE streamer_id = :id
             """

    def execute(self, binds, conn = None, transaction = False):

        self.dbi.processData(self.sql, binds, conn = conn,
                             transaction = transaction)
        return
