"""
_InsertRecoConfigs_

Oracle implementation of InsertRecoConfigs

Insert PromptReco configurations into Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertRecoConfigs(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """MERGE INTO reco_config
                 USING DUAL ON ( run = :RUN AND primds = :PRIMDS )
                 WHEN MATCHED THEN
                   UPDATE SET cmssw = :CMSSW,
                              scram_arch = :SCRAM_ARCH,
                              alca_skim = :ALCA_SKIM,
                              physics_skim = :PHYSICS_SKIM,
                              dqm_seq = :DQM_SEQ,
                              global_tag = :GLOBAL_TAG,
                              scenario = :SCENARIO,
                              proc_version = :PROC_VERSION,
                              multicore = :MULTICORE,
                              write_reco = :WRITE_RECO,
                              write_dqm = :WRITE_DQM,
                              write_aod = :WRITE_AOD,
                              write_miniaod = :WRITE_MINIAOD,
                              write_nanoaod = :WRITE_NANOAOD
                 WHEN NOT MATCHED THEN
                   INSERT (run, primds, cmssw, scram_arch, alca_skim,
                           physics_skim, dqm_seq, global_tag, scenario, proc_version,
                           multicore, write_reco, write_dqm,
                           write_aod, write_miniaod, write_nanoaod)
                   VALUES (:RUN, :PRIMDS, :CMSSW, :SCRAM_ARCH, :ALCA_SKIM,
                           :PHYSICS_SKIM, :DQM_SEQ, :GLOBAL_TAG, :SCENARIO, :PROC_VERSION,
                           :MULTICORE, :WRITE_RECO, :WRITE_DQM,
                           :WRITE_AOD, :WRITE_MINIAOD, :WRITE_NANOAOD)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
