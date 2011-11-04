"""
_InsertRepackConfig_

Oracle implementation of InsertRepackConfig

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertRepackConfig(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO repack_config
                 (RUN_ID, STREAM_ID, PROC_VERSION)
                 VALUES (:RUN,
                         (SELECT id FROM stream WHERE name = :STREAM),
                         :PROC_VER)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
