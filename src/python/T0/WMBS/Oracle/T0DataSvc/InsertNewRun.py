"""
_InsertNewRun_

Oracle implementation of InsertNewRun

Insert run info record into Tier0 Data Service

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertNewRun(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """MERGE INTO run_config
                 USING DUAL ON ( run = :RUN )
                 WHEN NOT MATCHED THEN
                   INSERT (run, acq_era)
                   VALUES (:RUN, :ACQ_ERA)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
