"""
_GetRunDatasetReleased_

Oracle implementation of GetRunDatasetReleased

Find run/dataset records where the PromptReco release is not in the Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetRunDatasetReleased(DBFormatter):

    sql = """SELECT reco_release_config.run_id AS run,
                    reco_release_config.primds_id AS primds_id
             FROM reco_release_config
             WHERE checkForZeroOneTwoState(reco_release_config.in_datasvc) = 1
             AND reco_release_config.released > 0
             """

    def execute(self, conn = None, transaction = False):

        results = self.dbi.processData(self.sql, binds = {}, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)
