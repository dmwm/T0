"""
_GetPrimaryDatasetConfigs_

Oracle implementation of GetPrimaryDatasetConfigs

Return reco configuration for each primary dataset and the run intervals where such configuration took place

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetPrimaryDatasetConfigs(DBFormatter):

    def execute(self, conn = None, transaction = False):


        sql = """SELECT primary_dataset.name AS primds, 
                        run.acq_era AS acq_era, 
                        MIN(run.run_id) AS min_run, 
                        MAX(run.run_id) AS max_run, 
                        cmssw_version.name AS cmssw, 
                        reco_config.global_tag AS global_tag, 
                        reco_config.physics_skim AS physics_skim, 
                        reco_config.dqm_seq AS dqm_seq
                FROM reco_config
                INNER JOIN run ON run.run_id = reco_config.run_id
                INNER JOIN primary_dataset ON primary_dataset.id = reco_config.primds_id
                INNER JOIN cmssw_version ON cmssw_version.id = reco_config.cmssw_id
                WHERE checkForZeroState(reco_config.in_datasvc) = 1
                GROUP BY primary_dataset.name, run.acq_era, cmssw_version.name,  reco_config.global_tag, reco_config.physics_skim, reco_config.dqm_seq
                ORDER BY primds, MIN(run.run_id) desc

                """

        results = self.dbi.processData(sql, binds = {}, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)