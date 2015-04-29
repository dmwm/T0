"""
_FindClosedLumis_

Oracle implementation of FindClosedLumis

Checking for closed run/stream/lumi with lumis above
a minimum threshold, extracting filecounts as well.

A lumi is considered closed if we have EoLS records
from every SM instance OR if we have EoLS records
from every SM instance except the ones that are not
supposed to have EoLS records anymore (because
the instance already has a EoR record with a max
lumi that is smaller than the current lumi).

Return a list of dictionaries with run/stream/lumi.

"""

from WMCore.Database.DBFormatter import DBFormatter

import logging
from sqlalchemy.exc import DatabaseError

class FindClosedLumis(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        # query has problems because of the way the join work
        # can create two groups for the same run/stream/lumi
        # first counting comparison doesn't work then
##         sql = """SELECT b.runnumber, a.stream, a.lumisection, SUM(a.filecount)
##                  FROM CMS_STOMGR.runs b
##                  LEFT OUTER JOIN CMS_STOMGR.streams a ON
##                    a.runnumber = b.runnumber AND
##                    a.instance = b.instance AND
##                    a.stream = :STREAM AND
##                    a.lumisection > :LUMI
##                  WHERE b.runnumber = :RUN
##                  GROUP BY b.runnumber, a.stream, a.lumisection
##                  HAVING COUNT(b.runnumber) = MAX(b.n_instances)
##                  AND (
##                    COUNT(a.runnumber) = COUNT(b.runnumber) OR
##                    COUNT(a.runnumber) = SUM(CASE
##                                               WHEN b.status = 1 THEN 1000
##                                               WHEN b.n_lumisections < a.lumisection THEN 0
##                                               ELSE 1
##                                             END)
##                  )
##                  """

        sql = """SELECT a.runnumber
                 FROM CMS_STOMGR.runs a
                 WHERE a.runnumber = :RUN
                 GROUP BY a.runnumber
                 HAVING COUNT(*) = MAX(a.n_instances)
                 """

        bindVars = []
        for b in binds:
            bindVars.append( { 'RUN' : b['RUN'] } )

        results = self.dbi.processData(sql, bindVars, conn = conn,
                                       transaction = transaction)[0].fetchall()

        goodRuns = []
        for result in results:
            goodRuns.append(result[0])

        bindVars = []
        for b in binds:
            if b['RUN'] in goodRuns:
                bindVars.append(b)

        if len(bindVars) == 0:
            return []

        sql = """SELECT a.runnumber, a.stream, a.lumisection, SUM(a.filecount)
                 FROM CMS_STOMGR.streams a
                 INNER JOIN CMS_STOMGR.runs b ON
                   b.runnumber = a.runnumber AND
                   b.instance = a.instance
                 WHERE a.runnumber = :RUN
                 AND a.stream = :STREAM
                 AND a.lumisection > :LUMI
                 GROUP BY a.runnumber, a.stream, a.lumisection
                 HAVING ( COUNT(*) = ( SELECT COUNT(*)
                                       FROM CMS_STOMGR.runs c
                                       WHERE c.runnumber = a.runnumber ) AND
                          COUNT(*) = ( SELECT MAX(c.n_instances)
                                       FROM CMS_STOMGR.runs c
                                       WHERE c.runnumber = a.runnumber ) )
                 OR ( COUNT(*) = SUM(CASE
                                       WHEN b.status = 1 THEN 1000
                                       WHEN b.n_lumisections < a.lumisection THEN 0
                                       ELSE 1
                                     END) AND
                      COUNT(*) = ( SELECT SUM(CASE
                                                WHEN c.status = 1 THEN 1000
                                                WHEN c.n_lumisections < a.lumisection THEN 0
                                                ELSE 1
                                              END)
                                          FROM CMS_STOMGR.runs c
                                          WHERE c.runnumber = a.runnumber ) )
                 """

        try:
            results = self.dbi.processData(sql, bindVars, conn = conn,
                                           transaction = transaction)[0].fetchall()
        except DatabaseError as ex:
            logging.error("ERROR: DatabaseError exception when checking for closed run/stream/lumi")
            logging.error("   %s" % ex)
            results = []

        closedLumis = []
        for result in results:
            closedLumis.append( { 'RUN' : result[0],
                                  'STREAM' : result[1],
                                  'LUMI' : result[2],
                                  'FILECOUNT' : result[3] } )

        return closedLumis
