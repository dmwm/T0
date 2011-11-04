"""
_UpdateStreamOverride_

Oracle implementation of UpdateStreamOverride

"""

from WMCore.Database.DBFormatter import DBFormatter

class UpdateStreamOverride(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """UPDATE ( SELECT override_version
                          FROM run_stream_cmssw_assoc
                          WHERE run_id = :RUN
                          AND stream_id = (SELECT id FROM stream WHERE name = :STREAM) ) a
                 SET a.override_version = (SELECT id FROM cmssw_version WHERE name = :OVERRIDE)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
