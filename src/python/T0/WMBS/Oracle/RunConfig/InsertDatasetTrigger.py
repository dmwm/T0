"""
_InsertDatasetTrigger_

Oracle implementation of InsertDatasetTrigger

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertDatasetTrigger(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO run_trig_primds_assoc
                 (RUN_ID, TRIG_ID, PRIMDS_ID)
                 VALUES (:RUN,
                         (SELECT id FROM trigger_label WHERE name = :TRIG),
                         (SELECT id FROM primary_dataset WHERE name = :PRIMDS))
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
