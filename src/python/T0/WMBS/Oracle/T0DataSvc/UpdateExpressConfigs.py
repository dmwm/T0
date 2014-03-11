"""
_UpdateExpressConfigs_

Oracle implementation of UpdateExpressConfigs

Mark Express configurations to be present in Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class UpdateExpressConfigs(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """UPDATE express_config
                 SET in_datasvc = 1
                 WHERE run_id = :RUN
                 AND stream_id = (SELECT id FROM stream WHERE name = :STREAM)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
