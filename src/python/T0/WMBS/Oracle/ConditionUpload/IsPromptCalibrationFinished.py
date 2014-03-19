"""
_IsPromptCalibrationFinished_

Oracle implementation of IsPromptCalibrationFinished

Figure out if PromptCalib is finished (input fileset
closed and no available or acquired files)

"""

from WMCore.Database.DBFormatter import DBFormatter

class IsPromptCalibrationFinished(DBFormatter):

    def execute(self, run, conn = None, transaction = False):

        sql = """SELECT 1
                 FROM prompt_calib
                 WHERE run_id = :RUN
                 HAVING COUNT(*) = SUM(finished)
                 """

        binds = { 'RUN' : run }

        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)[0].fetchall()

        return ( len(results) > 0 and results[0][0] == 1 )
