"""
_HaveAvailableFile_

Oracle implementation of HaveAvailableFile

For a given subscription check if there is an available file
"""

from WMCore.Database.DBFormatter import DBFormatter

class HaveAvailableFile(DBFormatter):

    sql = """SELECT 1
             FROM wmbs_sub_files_available
             WHERE wmbs_sub_files_available.subscription = :subscription
             AND ROWNUM = 1
             """

    def execute(self, subscription, conn = None, transaction = False):

        results = self.dbi.processData(self.sql, { 'subscription' : subscription },
                                       conn = conn, transaction = transaction)[0].fetchall()

        return ( len(results) > 0 and results[0][0] == 1 )
