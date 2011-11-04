"""
_GetPromptSkimConfig_

Oracle implementation of GetPromptSkimConfig

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetPromptSkimConfig(DBFormatter):

    def execute(self, run, stream = None, conn = None, transaction = False):

        sqlStream = """"""
        if stream != None:
            sqlStream = """AND run_primds_stream_assoc.stream_id =
                             (SELECT id FROM stream WHERE name = :STREAM)"""

        sql = """SELECT primary_dataset.name,
                        data_tier.name,
                        promptskim_config.skim_name,
                        storage_node.name,
                        cmssw_version.name,
                        promptskim_config.two_file_read,
                        promptskim_config.proc_version,
                        promptskim_config.global_tag,
                        promptskim_config.config_url
                 FROM promptskim_config
                 INNER JOIN run_primds_stream_assoc ON
                   run_primds_stream_assoc.run_id = promptskim_config.run_id AND
                   run_primds_stream_assoc.primds_id = promptskim_config.primds_id
                 INNER JOIN run_stream_style_assoc ON
                   run_stream_style_assoc.run_id = promptskim_config.run_id AND
                   run_stream_style_assoc.stream_id = run_primds_stream_assoc.stream_id AND
                   run_stream_style_assoc.style_id = (SELECT id FROM processing_style WHERE name = 'Bulk')
                 INNER JOIN primary_dataset ON
                   primary_dataset.id = promptskim_config.primds_id
                 INNER JOIN data_tier ON
                   data_tier.id = promptskim_config.tier_id
                 INNER JOIN storage_node ON
                   storage_node.id = promptskim_config.node_id
                 INNER JOIN cmssw_version ON
                   cmssw_version.id = promptskim_config.cmssw_id
                 WHERE promptskim_config.run_id = :RUN
                 %s """ % sqlStream

        binds = { 'RUN' : run }
        if stream != None:
            binds['STREAM'] = stream
        
        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)[0].fetchall()

        resultDict = {}
        for result in results:

            primds = result[0]
            tier = result[1]
            skim = result[2]

            if not resultDict.has_key(primds):
                resultDict[primds] = {}
            if not resultDict[primds].has_key(tier):
                resultDict[primds][tier] = {}

            resultDict[primds][tier][skim] = {}
            resultDict[primds][tier][skim]['node'] = result[3]
            resultDict[primds][tier][skim]['cmssw'] = result[4]
            resultDict[primds][tier][skim]['two_file_read'] = result[5]
            resultDict[primds][tier][skim]['proc_ver'] = result[6]
            resultDict[primds][tier][skim]['global_tag'] = result[7]
            resultDict[primds][tier][skim]['config_url'] = result[8]

        return resultDict
