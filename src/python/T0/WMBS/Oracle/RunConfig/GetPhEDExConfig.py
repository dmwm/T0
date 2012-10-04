"""
_GetPhEDExConfig_

Oracle implementation of GetPhEDExConfig

Returns PhEDEx configuration for given run and stream.

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetPhEDExConfig(DBFormatter):

    def execute(self, run, stream, conn = None, transaction = False):

        sql = """SELECT primary_dataset.name,
                        storage_node.name,
                        phedex_config.custodial,
                        phedex_config.request_only,
                        phedex_config.priority
                 FROM phedex_config
                 INNER JOIN run_primds_stream_assoc ON
                   run_primds_stream_assoc.run_id = phedex_config.run_id AND
                   run_primds_stream_assoc.primds_id = phedex_config.primds_id
                 INNER JOIN run_stream_style_assoc ON
                   run_stream_style_assoc.run_id = phedex_config.run_id AND
                   run_stream_style_assoc.stream_id = run_primds_stream_assoc.stream_id AND
                   run_stream_style_assoc.style_id = (SELECT id FROM processing_style WHERE name = 'Bulk')
                 INNER JOIN primary_dataset ON
                   primary_dataset.id = phedex_config.primds_id
                 INNER JOIN storage_node ON
                   storage_node.id = phedex_config.node_id
                 WHERE phedex_config.run_id = :RUN
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
            node = result[1]

            if not resultDict.has_key(primds):
                resultDict[primds] = {}

            resultDict[primds][node] = {}
            resultDict[primds][node]['custodial'] = result[2]
            resultDict[primds][node]['request_only'] = result[3]
            resultDict[primds][node]['priority'] = result[4]

        return resultDict
