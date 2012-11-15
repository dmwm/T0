"""
_GetPhEDExConfig_

Oracle implementation of GetPhEDExConfig

Returns PhEDEx configuration for given run and stream.

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetPhEDExConfig(DBFormatter):

    def execute(self, run, conn = None, transaction = False):

        sql = """SELECT primary_dataset.name,
                        storage_node.name,
                        phedex_config.custodial,
                        phedex_config.request_only,
                        phedex_config.priority
                 FROM run_primds_stream_assoc
                 INNER JOIN phedex_config ON
                   phedex_config.run_id = run_primds_stream_assoc.run_id AND
                   phedex_config.primds_id = run_primds_stream_assoc.primds_id
                 INNER JOIN primary_dataset ON
                   primary_dataset.id = phedex_config.primds_id
                 INNER JOIN storage_node ON
                   storage_node.id = phedex_config.node_id
                 WHERE run_primds_stream_assoc.run_id = :RUN
                 """

        binds = { 'RUN' : run }
        
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
