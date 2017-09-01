"""
_UpdateRecoReleaseConfigs_

Oracle implementation of UpdateRecoReleaseConfigs

Mark RecoRelease configurations to be present in Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class UpdateRecoReleaseConfigs(DBFormatter):

    sql = """UPDATE reco_release_config
             SET in_datasvc = :IN_DATASVC
             WHERE run_id = :RUN
             AND primds_id = :PRIMDS_ID
             """

    def execute(self, binds, conn = None, transaction = False):

        self.dbi.processData(self.sql, binds, conn = conn,
                             transaction = transaction)

        return
