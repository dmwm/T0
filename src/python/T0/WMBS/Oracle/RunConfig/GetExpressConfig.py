"""
_GetExpressConfig_

Oracle implementation of GetExpressConfig

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetExpressConfig(DBFormatter):

    def execute(self, run, stream, conn = None, transaction = False):

        sql = """SELECT express_config.proc_version AS proc_ver,
                        cmssw_version.name AS cmssw,
                        express_config.write_tiers AS write_tiers,
                        express_config.write_skims AS write_skims,
                        express_config.global_tag AS global_tag,
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
                 INNER JOIN cmssw_version ON
                   cmssw_version.id = run_stream_cmssw_assoc.override_version
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
