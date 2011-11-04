"""
_InsertTrigger_

Oracle implementation of InsertTrigger

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertTrigger(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO trigger_label
                 (ID, NAME)
                 SELECT trigger_label_SEQ.nextval, :TRIG
                 FROM DUAL
                 WHERE NOT EXISTS (
                   SELECT * FROM trigger_label
                   WHERE NAME = :TRIG
                 )"""

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
