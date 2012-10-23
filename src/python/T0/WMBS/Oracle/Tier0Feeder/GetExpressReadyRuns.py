"""
_GetExpressReadyRuns_

Oracle implementation of GetExpressReadyRuns

Checks the runs spefified for existence of
records in PopConLogDB and returns the one
where the record exist (and which therefore
can have Express released)

"""

from WMCore.Database.DBFormatter import DBFormatter

import logging
from sqlalchemy.exc import DatabaseError

class GetExpressReadyRuns(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """SELECT lastsince
                 FROM CMS_COND_31X_POPCONLOG.COND_LOG_TABLE
                 WHERE execmessage = 'OK'
                 AND iovtag like 'runinfo_start_%_hlt'
                 AND lastsince = :RUN
                 GROUP BY lastsince
                 HAVING COUNT(*) > 0
                 """

        try:
            results = self.dbi.processData(sql, binds, conn = conn,
                                           transaction = transaction)[0].fetchall()
        except DatabaseError, ex:
            logging.error("ERROR: DatabaseError exception when checking for express ready runs")
            logging.error("   %s" % ex)
            results = []

        runs = []
        for result in results:
            runs.append(result[0])

        return runs
