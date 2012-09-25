"""
_CompleteFiles_

Oracle implementation of CompleteFiles

"""

from WMCore.Database.DBFormatter import DBFormatter

class CompleteFiles(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO wmbs_sub_files_complete
                 (SUBSCRIPTION, FILEID)
                 VALUES (:SUBSCRIPTION, :FILEID)
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        sql = """DELETE FROM wmbs_sub_files_acquired
                 WHERE subscription = :SUBSCRIPTION
                 AND fileid = :FILEID"""

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
