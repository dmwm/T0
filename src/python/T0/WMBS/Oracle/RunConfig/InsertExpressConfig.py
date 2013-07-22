"""
_InsertExpressConfig_

Oracle implementation of InsertExpressConfig

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertExpressConfig(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO express_config
                 (RUN_ID, STREAM_ID, PROC_VERSION, WRITE_TIERS, GLOBAL_TAG,
                  MAX_EVENTS, MAX_SIZE, MAX_FILES, MAX_LATENCY, BLOCK_DELAY,
                  CMSSW_ID, ALCA_SKIM, DQM_SEQ)
                 VALUES (:RUN,
                         (SELECT id FROM stream WHERE name = :STREAM),
                         :PROC_VER,
                         :WRITE_TIERS,
                         :GLOBAL_TAG,
                         :MAX_EVENTS,
                         :MAX_SIZE,
                         :MAX_FILES,
                         :MAX_LATENCY,
                         :BLOCK_DELAY,
                         (SELECT id FROM cmssw_version WHERE name = :CMSSW),
                         :ALCA_SKIM,
                         :DQM_SEQ)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
