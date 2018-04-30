"""
_GetNewRun_

Oracle implementation of GetNewRun

Returns new runs and their acquisition era

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetNewRun(DBFormatter):

    def execute(self, conn = None, transaction = False):

        returnList = []

        sql = """SELECT run.run_id AS run,
                        run.acq_era AS acq_era
                 FROM run
                 WHERE checkForZeroState(run.in_datasvc) = 0
                 AND run.acq_era IS NOT NULL
                 """

        results = self.dbi.processData(sql, binds = {}, conn = conn,
                                       transaction = transaction)[0].fetchall()

        for result in results:
            returnList.append( { 'run': result[0],
                                 'acq_era': result[1] } )

        return returnList
