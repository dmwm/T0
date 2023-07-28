"""
_InsertPrimaryDatasetConfigs_

Oracle implementation of InsertPrimaryDatasetConfigs

Insert skipped streamers into Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertPrimaryDatasetConfigs(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """MERGE INTO primary_dataset_config
                 USING DUAL ON ( primds = :PRIMDS )
                 WHEN NOT MATCHED THEN
                   INSERT (primds, acq_era, run, cmssw, global_tag, physics_skim, dqm_seq)
                   VALUES (:PRIMDS, :ACQ_ERA, :RUN, :MAX_RUN, :CMSSW, :GLOBAL_TAG, :PHYSICS_SKIM, DQM_SEQ)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
