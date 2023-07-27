"""
_UpdatePrimaryDatasetConfig_

Oracle implementation of UpdatePrimaryDatasetConfig

Mark PromptReco configurations by primary dataset to be present in Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class UpdatePrimaryDatasetConfigs(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """UPDATE primary_dataset_config
                 SET in_datasvc = 1
                 WHERE primds_id = (SELECT id FROM primary_dataset WHERE name = :PRIMDS)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return