"""
_InsertRun_

Oracle implementation of InsertRun

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertRun(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO run
                 (RUN_ID, LAST_UPDATED, HLTKEY, START_TIME)
                 SELECT :RUN,
                        :TIME,
                        :HLTKEY,
                        :TIME
                 FROM DUAL
                 WHERE NOT EXISTS (
                   SELECT * FROM run WHERE run_id = :RUN
                 )"""

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
