"""
_InsertRecoConfig_

Oracle implementation of InsertRecoConfig

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertRecoConfig(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO reco_config
                 (RUN_ID, PRIMDS_ID, DO_RECO, RECO_SPLIT, WRITE_RECO, WRITE_DQM,
                  WRITE_AOD, WRITE_MINIAOD, PROC_VERSION, ALCA_SKIM, PHYSICS_SKIM,
                  DQM_SEQ, CMSSW_ID, MULTICORE, SCRAM_ARCH, GLOBAL_TAG)
                 VALUES (:RUN,
                         (SELECT id FROM primary_dataset WHERE name = :PRIMDS),
                         :DO_RECO,
                         :RECO_SPLIT,
                         :WRITE_RECO,
                         :WRITE_DQM,
                         :WRITE_AOD,
                         :WRITE_MINIAOD,
                         :PROC_VER,
                         :ALCA_SKIM,
                         :PHYSICS_SKIM,
                         :DQM_SEQ,
                         (SELECT id FROM cmssw_version WHERE name = :CMSSW),
                         :MULTICORE,
                         :SCRAM_ARCH,
                         :GLOBAL_TAG)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
