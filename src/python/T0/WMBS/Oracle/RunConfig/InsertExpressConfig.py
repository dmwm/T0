"""
_InsertExpressConfig_

Oracle implementation of InsertExpressConfig

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertExpressConfig(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO express_config
                 (RUN_ID, STREAM_ID, PROC_VERSION, WRITE_TIERS, WRITE_DQM, GLOBAL_TAG,
                  MAX_RATE, MAX_EVENTS, MAX_SIZE, MAX_FILES, MAX_LATENCY, DQM_INTERVAL,
                  CMSSW_ID, SCRAM_ARCH, RECO_CMSSW_ID,RECO_SCRAM_ARCH, DATA_TYPE,
                  MULTICORE, ALCA_SKIM, DQM_SEQ)
                 VALUES (:RUN,
                         (SELECT id FROM stream WHERE name = :STREAM),
                         :PROC_VER,
                         :WRITE_TIERS,
                         :WRITE_DQM,
                         :GLOBAL_TAG,
                         :MAX_RATE,
                         :MAX_EVENTS,
                         :MAX_SIZE,
                         :MAX_FILES,
                         :MAX_LATENCY,
                         :DQM_INTERVAL,
                         (SELECT id FROM cmssw_version WHERE name = :CMSSW),
                         :SCRAM_ARCH,
                         (SELECT id FROM cmssw_version WHERE name = :RECO_CMSSW),
                         :RECO_SCRAM_ARCH,
                         :DATA_TYPE,
                         :MULTICORE,
                         :ALCA_SKIM,
                         :DQM_SEQ)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
