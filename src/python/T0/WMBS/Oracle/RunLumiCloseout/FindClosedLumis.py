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
            results = self.dbi.processData(sql, binds, conn = conn,
                                           transaction = transaction)[0].fetchall()
        except DatabaseError, ex:
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
