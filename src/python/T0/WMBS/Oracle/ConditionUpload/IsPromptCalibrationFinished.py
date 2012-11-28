"""
_IsPromptCalibrationFinished_

Oracle implementation of IsPromptCalibrationFinished

Figure out if PromptCalib is finished (input fileset
closed and no available or acquired files)

"""

from WMCore.Database.DBFormatter import DBFormatter

class IsPromptCalibrationFinished(DBFormatter):

    def execute(self, subscription, conn = None, transaction = False):

        sql = """SELECT 1
                 FROM wmbs_subscription
                   INNER JOIN wmbs_fileset ON
                     wmbs_fileset.id = wmbs_subscription.fileset
                   LEFT OUTER JOIN wmbs_sub_files_available ON
                     wmbs_sub_files_available.subscription = wmbs_subscription.id
                   LEFT OUTER JOIN wmbs_sub_files_acquired ON
                     wmbs_sub_files_acquired.subscription = wmbs_subscription.id
                 WHERE wmbs_subscription.id = :SUBSCRIPTION
                 HAVING COUNT(wmbs_sub_files_available.subscription) = 0
                 AND COUNT(wmbs_sub_files_acquired.subscription) = 0
                 AND SUM(wmbs_fileset.open) = 0
                 """

        binds = { 'SUBSCRIPTION' : subscription }

        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)[0].fetchall()

        return ( len(results) > 0 and results[0][0] == 1 )
