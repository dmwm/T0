"""
_FindHighContLumi_

Oracle implementation of FindHighContLumi

Find all run and stream combinations that are
configured and active (run/stream fileset is open).
For each of these find the highest lumi where
all lumis from 1 up to that lumi have
lumi_section_closed records.

This is all done server side using Oracle analytic
functions to detect 'holes' in the sequence for
lumis for a run/stream. Will return 0 for a run/stream
combo without any lumis. Will return 0 if lumi 1 is
missing. If all lumis are in a continious sequence
it returns the largest lumi.

LEAD is used to also return the next lumi together
with the current (for comparison). MIN is used so
we keep the minimum value of the sequence (the normal
checks don't work if the sequence does not start at 1).
Finally, the LEFT OUTER JOIN ensures that we can
detect run/stream without any lumis.

Return a list of dictionaries with run/stream/lumi.

"""

from WMCore.Database.DBFormatter import DBFormatter

class FindHighContLumi(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT a.run_id, stream.name, a.lumi_id
                 FROM (
                   SELECT run_id AS run_id,
                          stream_id AS stream_id,
                          CASE
                            WHEN MIN(min_lumi) = 1 THEN NVL(MIN(current_lumi),0)
                            ELSE 0
                          END AS lumi_id
                   FROM (
                     SELECT run_stream_fileset_assoc.run_id AS run_id,
                            run_stream_fileset_assoc.stream_id AS stream_id,
                            lumi_section_closed.lumi_id AS current_lumi,
                            LEAD(lumi_section_closed.lumi_id, 1, NULL)
                              OVER (PARTITION BY run_stream_fileset_assoc.run_id,
                                                 run_stream_fileset_assoc.stream_id
                                    ORDER BY lumi_section_closed.lumi_id) AS next_lumi,
                            MIN(lumi_section_closed.lumi_id)
                              OVER (PARTITION BY run_stream_fileset_assoc.run_id,
                                                 run_stream_fileset_assoc.stream_id
                                    ORDER BY lumi_section_closed.lumi_id) AS min_lumi
                     FROM run_stream_fileset_assoc
                     INNER JOIN wmbs_fileset ON
                       wmbs_fileset.id = run_stream_fileset_assoc.fileset AND
                       wmbs_fileset.open = 1
                     LEFT OUTER JOIN lumi_section_closed ON
                       lumi_section_closed.run_id = run_stream_fileset_assoc.run_id AND
                       lumi_section_closed.stream_id = run_stream_fileset_assoc.stream_id
                   )
                   WHERE current_lumi + 1 != next_lumi OR next_lumi IS NULL
                   GROUP BY run_id, stream_id
                 ) a
                 INNER JOIN stream ON
                   stream.id = a.stream_id
                 """

        results = self.dbi.processData(sql, {}, conn = conn,
                                       transaction = transaction)[0].fetchall()

        runStreamLumis = []
        for result in results:
            runStreamLumis.append( { 'RUN' : result[0],
                                     'STREAM' : result[1],
                                     'LUMI' : result[2] } )

        return runStreamLumis
