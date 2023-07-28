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
                      reco_config.primds_id AS primds, 
                      run.acq_era AS acq_era, 
                      run.run_id AS run,
                      reco_config.cmssw_id AS cmssw, 
                      reco_config.global_tag AS global_tag, 
                      reco_config.physics_skim AS physics_skim, 
                      reco_config.dqm_seq AS dqm_seq
                FROM reco_config
                JOIN run ON run.run_id = reco_config.run_id
                WHERE reco_config.in_datasvc = 1
                ORDER BY primds, run desc
                """

        results = self.dbi.processData(sql, binds = {}, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)