"""
_InsertExpressConfigs_

Oracle implementation of InsertExpressConfigs

Insert Express configurations into Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertExpressConfigs(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """MERGE INTO express_config
                 USING DUAL ON ( run = :RUN AND stream = :STREAM )
                 WHEN MATCHED THEN
                   UPDATE SET cmssw = :CMSSW,
                              scram_arch = :SCRAM_ARCH,
                              reco_cmssw = :RECO_CMSSW,
                              reco_scram_arch = :RECO_SCRAM_ARCH,
                              scenario = :SCENARIO
                 WHEN NOT MATCHED THEN
                   INSERT (run, stream, cmssw, scram_arch, reco_cmssw,
                           reco_scram_arch, global_tag, scenario)
                   VALUES (:RUN, :STREAM, :CMSSW, :SCRAM_ARCH, :RECO_CMSSW,
                           :RECO_SCRAM_ARCH, :GLOBAL_TAG, :SCENARIO)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
