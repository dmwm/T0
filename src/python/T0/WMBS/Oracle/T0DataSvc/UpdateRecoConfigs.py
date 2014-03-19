"""
_UpdateRecoConfigs_

Oracle implementation of UpdateRecoConfigs

Mark PromptReco configurations to be present in Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class UpdateRecoConfigs(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """UPDATE reco_config
                 SET in_datasvc = 1
                 WHERE run_id = :RUN
                 AND primds_id = (SELECT id FROM primary_dataset WHERE name = :PRIMDS)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
