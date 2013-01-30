"""
_MarkStreamersFinished_

Oracle implementation of MarkStreamersFinished

Just updates the streamer status to finished, ie.
completely processed and SM notified about it.
Use the deleted column for now because it's
there and unused.

"""

from WMCore.Database.DBFormatter import DBFormatter

class MarkStreamersFinished(DBFormatter):

    def execute(self, streamerids, conn = None, transaction = False):

        sql = """UPDATE streamer
                 SET deleted = 1
                 WHERE id = :ID
                 """

        binds = []
        for streamerid in streamerids:
            binds.append( { 'ID' : streamerid } )

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
