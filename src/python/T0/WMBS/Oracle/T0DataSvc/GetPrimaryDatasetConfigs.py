"""
_GetPrimaryDatasetConfigs_

Oracle implementation of GetPrimaryDatasetConfigs

Return reco configuration for each primary dataset and the run intervals where such configuration took place

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetPrimaryDatasetConfigs(DBFormatter):

    def execute(self, conn = None, transaction = False):


        sql = """
                SELECT 
                      primary_dataset_config.primds_id AS primds, 
                      primary_dataset_config.acq_era AS acq_era, 
                      MIN(run.run_id) AS min_run, 
                      MAX(run.run_id) AS max_run, 
                      primary_dataset_config.cmssw_id AS cmssw, 
                      primary_dataset_config.global_tag AS global_tag, 
                      primary_dataset_config.physics_skim AS physics_skim, 
                      primary_dataset_config.dqm_seq AS dqm_seq
                FROM primary_dataset_config
                JOIN run ON run.run_id = primary_dataset_config.run_id
                WHERE checkForZeroState(primary_dataset_config.in_datasvc) = 0
                GROUP BY acq_era, primds, cmssw,  global_tag, physics_skim, dqm_seq
                ORDER BY primds, min_run desc
                """

        results = self.dbi.processData(sql, binds = {}, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)