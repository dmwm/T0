"""
_InsertEventScenarios_

Oracle implementation of InsertEventScenarios

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertEventScenarios(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """MERGE INTO EVENT_SCENARIO
                 USING (
                    SELECT COALESCE(MAX(ID), 0) + 1 AS NEW_ID FROM EVENT_SCENARIO
                    ) 
                 ON (EVENT_SCENARIO.NAME = :SCENARIO)
                 WHEN NOT MATCHED THEN
                     INSERT (ID, NAME) VALUES (NEW_ID, :SCENARIO)

                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return

