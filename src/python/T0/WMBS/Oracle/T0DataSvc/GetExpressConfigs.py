"""
_GetExpressConfigs_

Oracle implementation of GetExpressConfigs

Returns Express configurations which are not in the Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetExpressConfigs(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT express_config.run_id AS run,
                        stream.name AS stream,
                        stream_version.name AS cmssw,
                        express_config.scram_arch AS scram_arch,
                        reco_version.name AS reco_cmssw,
                        express_config.reco_scram_arch AS reco_scram_arch,
                        express_config.alca_skim AS alca_skim,
                        express_config.dqm_seq AS dqm_seq,
                        express_config.global_tag AS global_tag,
                        event_scenario.name AS scenario,
                        express_config.multicore AS multicore,
                        express_config.write_tiers AS write_tiers,
                        express_config.write_dqm AS write_dqm
                 FROM express_config
                 INNER JOIN stream ON
                   stream.id = express_config.stream_id
                 INNER JOIN cmssw_version stream_version ON
                   stream_version.id = express_config.cmssw_id
                 LEFT OUTER JOIN cmssw_version reco_version ON
                   reco_version.id = express_config.reco_cmssw_id
                 INNER JOIN stream_special_primds_assoc ON
                   stream_special_primds_assoc.stream_id = express_config.stream_id
                 INNER JOIN run_primds_scenario_assoc ON
                   run_primds_scenario_assoc.run_id = express_config.run_id AND
                   run_primds_scenario_assoc.primds_id = stream_special_primds_assoc.primds_id
                 INNER JOIN event_scenario ON
                   event_scenario.id = run_primds_scenario_assoc.scenario_id
                 WHERE checkForZeroState(express_config.in_datasvc) = 0
                 """

        results = self.dbi.processData(sql, binds = {}, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)
