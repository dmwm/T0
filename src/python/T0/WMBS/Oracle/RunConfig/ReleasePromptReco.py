"""
_ReleasePromptReco_
Oracle implementation of ReleasePromptReco
Release PromptReco for given run and primary dataset.
"""

from WMCore.Database.DBFormatter import DBFormatter

class ReleasePromptReco(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """UPDATE reco_release_config
                 SET released = :NOW
                 WHERE run_id = :RUN
                 AND primds_id = (SELECT id FROM primary_dataset WHERE name = :PRIMDS)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
