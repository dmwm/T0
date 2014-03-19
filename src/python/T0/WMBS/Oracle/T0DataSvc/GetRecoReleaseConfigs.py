"""
_GetRecoReleaseConfigs_

Oracle implementation of GetRecoReleaseConfigs

Return RecoRelease configurations which are not in the Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetRecoReleaseConfigs(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT run_id AS run,
                        MAX(released) AS released
                        FROM (
                          SELECT run_id, primds_id, in_datasvc, released
                          FROM reco_release_config
                          WHERE checkForZeroOneState(in_datasvc) = 0
                          OR ( checkForZeroOneState(in_datasvc) = 1 AND released > 0 )
                        )
                        GROUP BY run_id
                        """

        results = self.dbi.processData(sql, binds = {}, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)
