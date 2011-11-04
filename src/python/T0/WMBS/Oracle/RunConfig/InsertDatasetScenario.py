"""
_InsertDatasetScenario_

Oracle implementation of InsertDatasetScenario

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertDatasetScenario(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO run_primds_scenario_assoc
                 (RUN_ID, PRIMDS_ID, SCENARIO_ID)
                 VALUES (:RUN,
                         (SELECT id FROM primary_dataset WHERE name = :PRIMDS),
                         (SELECT id FROM event_scenario WHERE name = :SCENARIO))
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
