"""
_InsertPromptSkimConfig_

Oracle implementation of InsertPromptSkimConfig

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertPromptSkimConfig(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO promptskim_config
                 (RUN_ID, PRIMDS_ID, TIER_ID, SKIM_NAME, NODE_ID, CMSSW_ID,
                  TWO_FILE_READ, PROC_VERSION, GLOBAL_TAG, CONFIG_URL)
                 VALUES (:RUN,
                         (SELECT id FROM primary_dataset WHERE name = :PRIMDS),
                         (SELECT id FROM data_tier WHERE name = :TIER),
                         :SKIM_NAME,
                         (SELECT id FROM storage_node WHERE name = :NODE),
                         (SELECT id FROM cmssw_version WHERE name = :CMSSW),
                         :TWO_FILE_READ,
                         :PROC_VER,
                         :GLOBAL_TAG,
                         :CONFIG_URL)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)
        return
