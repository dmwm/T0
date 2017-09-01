"""
_GetPhEDExConfig_

Oracle implementation of GetPhEDExConfig

Returns PhEDEx configuration for given run and stream.

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetPhEDExConfig(DBFormatter):

    sql = """SELECT primary_dataset.name,
                    archival_node.name,
                    tape_node.name,
                    disk_node.name,
                    disk_node_reco.name
             FROM phedex_config
             INNER JOIN primary_dataset ON
               primary_dataset.id = phedex_config.primds_id
             LEFT OUTER JOIN storage_node archival_node ON
               archival_node.id = phedex_config.archival_node_id
             LEFT OUTER JOIN storage_node tape_node ON
               tape_node.id = phedex_config.tape_node_id
             LEFT OUTER JOIN storage_node disk_node ON
               disk_node.id = phedex_config.disk_node_id
             LEFT OUTER JOIN storage_node disk_node_reco ON
               disk_node_reco.id = phedex_config.disk_node_reco_id
             WHERE phedex_config.run_id = :RUN
             """

    def execute(self, run, conn = None, transaction = False):

        binds = { 'RUN' : run }
        
        results = self.dbi.processData(self.sql, binds, conn = conn,
                                       transaction = transaction)[0].fetchall()

        resultDict = {}
        for result in results:

            primds = result[0]

            if primds not in resultDict:
                resultDict[primds] = {}

            resultDict[primds]['archival_node'] = result[1]
            resultDict[primds]['tape_node'] = result[2]
            resultDict[primds]['disk_node'] = result[3]
            resultDict[primds]['disk_node_reco'] = result[4]

        return resultDict
