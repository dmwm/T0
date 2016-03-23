"""
_CloseRunStreamFilesets_

Oracle implementation of CloseRunStreamFilesets

If a run has stopped (run summary), is closed (storage manager) and the
run/stream fileset is still open, check for complete lumi_closed records,
that all lumis are finally closed (all data for them in T0AST) and that
all data has been feed to the filesets for processing.

If all these conditions are satisifed, close the run/stream fileset.

"""
import time

from WMCore.Database.DBFormatter import DBFormatter

class CloseRunStreamFilesets(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """MERGE INTO wmbs_fileset a
                 USING (
                   SELECT b.run_id AS run_id,
                          b.stream_id AS stream_id,
                          b.fileset AS fileset
                   FROM (
                     SELECT run_stream_fileset_assoc.run_id AS run_id,
                            run_stream_fileset_assoc.stream_id AS stream_id,
                            run_stream_fileset_assoc.fileset AS fileset
                     FROM run_stream_fileset_assoc
                     INNER JOIN wmbs_fileset ON
                       wmbs_fileset.id = run_stream_fileset_assoc.fileset AND
                       wmbs_fileset.open = 1
                     INNER JOIN run ON
                       run.run_id = run_stream_fileset_assoc.run_id AND
                       run.stop_time > 0 AND
                       run.close_time > 0
                     INNER JOIN lumi_section_closed ON
                       lumi_section_closed.run_id = run_stream_fileset_assoc.run_id AND
                       lumi_section_closed.stream_id = run_stream_fileset_assoc.stream_id
                     GROUP BY run_stream_fileset_assoc.run_id,
                              run_stream_fileset_assoc.stream_id,
                              run_stream_fileset_assoc.fileset
                     HAVING SUM(CASE
                                  WHEN lumi_section_closed.close_time = 0 THEN 0
                                  ELSE 1
                                END) = MAX(lumi_section_closed.lumi_id)
                     AND MAX(lumi_section_closed.lumi_id) = MAX(run.lumicount)
                   ) b
                   LEFT OUTER JOIN streamer ON
                     streamer.run_id = b.run_id AND
                     streamer.stream_id = b.stream_id AND
                     checkForZeroState(streamer.used) = 0
                   WHERE streamer.run_id IS NULL
                   GROUP BY b.run_id,
                            b.stream_id,
                            b.fileset
                 ) c ON ( c.fileset = a.id )
                 WHEN MATCHED THEN
                   UPDATE SET a.open = 0,
                              a.last_update = :CLOSE_TIME
                 """

        binds = { 'CLOSE_TIME' : int(time.time()) }

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
