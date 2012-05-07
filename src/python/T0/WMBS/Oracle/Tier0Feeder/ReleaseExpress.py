"""
_ReleaseExpress_

Oracle implementation of ReleaseExpress

Release express for the runs specified

"""

from WMCore.Database.DBFormatter import DBFormatter

class ReleaseExpress(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """UPDATE run
                 SET express_released = 1
                 WHERE run_id = :RUN
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
