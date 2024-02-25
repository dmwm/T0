"""
_GetRunSetup_

Oracle implementation of GetRunSetup

Retrieve run setup information about run from online sources

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetRunSetup(DBFormatter):

    def execute(self, run, conn = None, transaction = False):

        binds = { 'RUN' : run }

        sql = """SELECT SETUPLABEL FROM CMS_STOMGR.RUNS
                 WHERE CMS_STOMGR.RUNS.RUNNUMBER = :RUN
                 """
        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)

        return self.formatOne(results)[0]