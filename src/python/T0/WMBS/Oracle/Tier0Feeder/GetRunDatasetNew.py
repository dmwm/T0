"""
_GetRunDatasetNew_

Oracle implementation of GetRunDatasetNew

Find new run/dataset records not in the Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetRunDatasetNew(DBFormatter):

    sql = """SELECT reco_release_config.run_id AS run,
                    reco_release_config.primds_id AS primds_id,
                    primary_dataset.name AS primds
             FROM reco_release_config
             INNER JOIN primary_dataset ON
               primary_dataset.id = reco_release_config.primds_id
             WHERE checkForZeroOneTwoState(reco_release_config.in_datasvc) = 0
             """

    def execute(self, conn = None, transaction = False):

        results = self.dbi.processData(self.sql, binds = {}, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)
