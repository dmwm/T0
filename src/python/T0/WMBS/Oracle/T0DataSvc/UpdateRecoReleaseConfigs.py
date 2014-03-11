"""
_UpdateRecoConfigs_

Oracle implementation of UpdateRecoConfigs

Mark RecoRelease configurations to be present in Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class UpdateRecoReleaseConfigs(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """UPDATE reco_release_config
                 SET in_datasvc = :IN_DATASVC
                 WHERE run_id = :RUN
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
