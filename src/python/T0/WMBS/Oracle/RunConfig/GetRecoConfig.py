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
                        cmssw_version.name,
                        reco_config.reco_split,
                        reco_config.write_reco,
                        reco_config.write_aod,
                        reco_config.write_dqm,
                        reco_config.proc_version,
                        reco_config.alca_skim,
                        reco_config.dqm_seq,
                        reco_config.global_tag,
                        event_scenario.name
                 FROM reco_config
                 INNER JOIN run_primds_stream_assoc ON
                   run_primds_stream_assoc.run_id = reco_config.run_id AND
                   run_primds_stream_assoc.primds_id = reco_config.primds_id
                 INNER JOIN run_stream_style_assoc ON
                   run_stream_style_assoc.run_id = reco_config.run_id AND
                   run_stream_style_assoc.stream_id = run_primds_stream_assoc.stream_id AND
                   run_stream_style_assoc.style_id = (SELECT id FROM processing_style WHERE name = 'Bulk')
                 INNER JOIN run_primds_scenario_assoc ON
                   run_primds_scenario_assoc.run_id = reco_config.run_id AND
                   run_primds_scenario_assoc.primds_id = reco_config.primds_id
                 INNER JOIN primary_dataset ON
                   primary_dataset.id = run_primds_stream_assoc.primds_id
                 INNER JOIN cmssw_version ON
                   cmssw_version.id = reco_config.cmssw_id
                 INNER JOIN event_scenario ON
                   event_scenario.id = run_primds_scenario_assoc.scenario_id
                 WHERE reco_config.run_id = :RUN
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
            resultDict[primds]['cmssw'] = result[2]
            resultDict[primds]['reco_split'] = result[3]
            resultDict[primds]['write_reco'] = result[4]
            resultDict[primds]['write_aod'] = result[5]
            resultDict[primds]['write_dqm'] = result[6]
            resultDict[primds]['proc_ver'] = result[7]
            resultDict[primds]['alca_skim'] = result[8]
            resultDict[primds]['dqm_seq'] = result[9]
            resultDict[primds]['global_tag'] = result[10]
            resultDict[primds]['scenario'] = result[11]

        return resultDict
