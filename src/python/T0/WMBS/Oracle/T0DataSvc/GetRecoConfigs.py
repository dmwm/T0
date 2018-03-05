"""
_GetRecoConfigs_

Oracle implementation of GetRecoConfigs

Return PromptReco configurations which are not in the Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetRecoConfigs(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT reco_config.run_id AS run,
                        primary_dataset.name AS primds,
                        cmssw_version.name AS cmssw,
                        reco_config.scram_arch AS scram_arch,
                        reco_config.alca_skim AS alca_skim,
                        reco_config.physics_skim AS physics_skim,
                        reco_config.dqm_seq AS dqm_seq,
                        reco_config.global_tag AS global_tag,
                        event_scenario.name AS scenario,
                        reco_config.multicore AS multicore,
                        reco_config.write_reco AS write_reco,
                        reco_config.write_dqm AS write_dqm,
                        reco_config.write_aod AS write_aod,
                        reco_config.write_miniaod AS write_miniaod
                 FROM reco_config
                 INNER JOIN primary_dataset ON
                   primary_dataset.id = reco_config.primds_id
                 INNER JOIN cmssw_version ON
                   cmssw_version.id = reco_config.cmssw_id
                 INNER JOIN run_primds_scenario_assoc ON
                   run_primds_scenario_assoc.run_id = reco_config.run_id AND
                   run_primds_scenario_assoc.primds_id = reco_config.primds_id
                 INNER JOIN event_scenario ON
                   event_scenario.id = run_primds_scenario_assoc.scenario_id
                 WHERE checkForZeroState(reco_config.in_datasvc) = 0
                 """

        results = self.dbi.processData(sql, binds = {}, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)
