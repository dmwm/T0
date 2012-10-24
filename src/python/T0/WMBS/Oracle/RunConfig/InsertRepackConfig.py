"""
_InsertRepackConfig_

Oracle implementation of InsertRepackConfig

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertRepackConfig(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO repack_config
                 (RUN_ID, STREAM_ID, PROC_VERSION, MAX_SIZE_SINGLE_LUMI, MAX_SIZE_MULTI_LUMI,
                  MIN_SIZE, MAX_SIZE, MAX_EDM_SIZE, MAX_OVER_SIZE, MAX_EVENTS, MAX_FILES)
                 VALUES (:RUN,
                         (SELECT id FROM stream WHERE name = :STREAM),
                         :PROC_VER,
                         :MAX_SIZE_SINGLE_LUMI,
                         :MAX_SIZE_MULTI_LUMI,
                         :MIN_SIZE,
                         :MAX_SIZE,
                         :MAX_EDM_SIZE,
                         :MAX_OVER_SIZE,
                         :MAX_EVENTS,
                         :MAX_FILES)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
