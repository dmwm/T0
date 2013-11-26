"""
_GetExpressConfig_

Oracle implementation of GetExpressConfig

Returns express configuration for given run and stream.

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetExpressConfig(DBFormatter):

    def execute(self, run, stream, conn = None, transaction = False):

        sql = """SELECT express_config.proc_version AS proc_ver,
                        stream_version.name AS stream_cmssw,
                        express_config.write_tiers AS write_tiers,
                        express_config.global_tag AS global_tag,
                        express_config.max_events AS max_events,
                        express_config.max_size AS max_size,
                        express_config.max_files AS max_files,
                        express_config.max_latency AS max_latency,
                        reco_version.name AS reco_cmssw,
                        express_config.alca_skim AS alca_skim,
                        express_config.dqm_seq AS dqm_seq,
                        event_scenario.name AS scenario
                 FROM express_config
                 INNER JOIN run_stream_cmssw_assoc ON
                   run_stream_cmssw_assoc.run_id = express_config.run_id AND
                   run_stream_cmssw_assoc.stream_id = express_config.stream_id
                 INNER JOIN stream_special_primds_assoc ON
                   stream_special_primds_assoc.stream_id = express_config.stream_id
                 INNER JOIN run_primds_scenario_assoc ON
                   run_primds_scenario_assoc.run_id = express_config.run_id AND
                   run_primds_scenario_assoc.primds_id = stream_special_primds_assoc.primds_id
                 INNER JOIN cmssw_version stream_version ON
                   stream_version.id = run_stream_cmssw_assoc.override_version
                 LEFT OUTER JOIN cmssw_version reco_version ON
                   reco_version.id = express_config.cmssw_id
                 INNER JOIN event_scenario ON
                   event_scenario.id = run_primds_scenario_assoc.scenario_id
                 WHERE express_config.run_id = :RUN
                 AND express_config.stream_id = (SELECT id FROM stream WHERE name = :STREAM)
                 """

        binds = { 'RUN' : run,
                  'STREAM' : stream }

        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)[0]
