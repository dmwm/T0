"""
_InsertRecoConfig_

Oracle implementation of InsertRecoConfig

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertRecoConfig(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO reco_config
                 (RUN_ID, PRIMDS_ID, DO_RECO, CMSSW_ID, RECO_SPLIT, WRITE_RECO,
                  WRITE_DQM, WRITE_AOD, PROC_VERSION, ALCA_SKIM, DQM_SEQ, GLOBAL_TAG)
                 VALUES (:RUN,
                         (SELECT id FROM primary_dataset WHERE name = :PRIMDS),
                         :DO_RECO,
                         (SELECT id FROM cmssw_version WHERE name = :CMSSW),
                         :RECO_SPLIT,
                         :WRITE_RECO,
                         :WRITE_DQM,
                         :WRITE_AOD,
                         :PROC_VER,
                         :ALCA_SKIM,
                         :DQM_SEQ,
                         :GLOBAL_TAG)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
