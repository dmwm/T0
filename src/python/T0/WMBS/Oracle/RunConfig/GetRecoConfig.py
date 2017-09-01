"""
_GetRecoConfig_

Oracle implementation of GetRecoConfig

Return PromptReco configuration for given run and stream.

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetRecoConfig(DBFormatter):

    def execute(self, run, stream, conn = None, transaction = False):

        sql = """SELECT primary_dataset.name,
                        reco_config.do_reco,
                        reco_config.reco_split,
                        reco_config.write_reco,
                        reco_config.write_aod,
                        reco_config.write_miniaod,
                        reco_config.write_dqm,
                        reco_config.proc_version,
                        reco_config.alca_skim,
                        reco_config.dqm_seq,
                        cmssw_version.name,
                        reco_config.scram_arch,
                        reco_config.multicore,
                        reco_config.global_tag,
                        event_scenario.name
                 FROM run_primds_stream_assoc
                 INNER JOIN reco_config ON
                   reco_config.run_id = run_primds_stream_assoc.run_id AND
                   reco_config.primds_id = run_primds_stream_assoc.primds_id
                 INNER JOIN run_primds_scenario_assoc ON
                   run_primds_scenario_assoc.run_id = run_primds_stream_assoc.run_id AND
                   run_primds_scenario_assoc.primds_id = reco_config.primds_id
                 INNER JOIN primary_dataset ON
                   primary_dataset.id = run_primds_stream_assoc.primds_id
                 INNER JOIN cmssw_version ON
                   cmssw_version.id = reco_config.cmssw_id
                 INNER JOIN event_scenario ON
                   event_scenario.id = run_primds_scenario_assoc.scenario_id
                 WHERE run_primds_stream_assoc.run_id = :RUN
                 AND run_primds_stream_assoc.stream_id =
                   (SELECT id FROM stream WHERE name = :STREAM)
                 """

        binds = { 'RUN' : run,
                  'STREAM' : stream }
        
        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)[0].fetchall()

        resultDict = {}
        for result in results:

            primds = result[0]

            resultDict[primds] = {}
            resultDict[primds]['do_reco'] = result[1]
            resultDict[primds]['reco_split'] = result[2]
            resultDict[primds]['write_reco'] = result[3]
            resultDict[primds]['write_aod'] = result[4]
            resultDict[primds]['write_miniaod'] = result[5]
            resultDict[primds]['write_dqm'] = result[6]
            resultDict[primds]['proc_ver'] = result[7]
            resultDict[primds]['alca_skim'] = result[8]
            resultDict[primds]['dqm_seq'] = result[9]
            resultDict[primds]['cmssw'] = result[10]
            resultDict[primds]['scram_arch'] = result[11]
            resultDict[primds]['multicore'] = result[12]
            resultDict[primds]['global_tag'] = result[13]
            resultDict[primds]['scenario'] = result[14]

        return resultDict
