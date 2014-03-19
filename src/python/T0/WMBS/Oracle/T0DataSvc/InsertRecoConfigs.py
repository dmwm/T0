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
                              global_tag = :GLOBAL_TAG,
                              scenario = :SCENARIO
                 WHEN NOT MATCHED THEN
                   INSERT (run, primds, cmssw, scram_arch,
                           global_tag, scenario)
                   VALUES (:RUN, :PRIMDS, :CMSSW, :SCRAM_ARCH,
                           :GLOBAL_TAG, :SCENARIO)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
