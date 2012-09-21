"""
_HaveJobGroup_

Oracle implementation of HaveJobGroup

For a given subscription check if there is an existing job group
"""

from WMCore.Database.DBFormatter import DBFormatter

class HaveJobGroup(DBFormatter):

    sql = """SELECT 1
             FROM wmbs_jobgroup
             WHERE wmbs_jobgroup.subscription = :subscription
             AND ROWNUM = 1
             """

    def execute(self, subscription, conn = None, transaction = False):

        results = self.dbi.processData(self.sql, { 'subscription' : subscription },
                                       conn = conn, transaction = transaction)[0].fetchall()

        return ( len(results) > 0 and results[0][0] == 1 )
