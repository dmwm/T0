"""
_CloseRunStreamFilesets_

Oracle implementation of CloseRunStreamFilesets



"""
import time

from WMCore.Database.DBFormatter import DBFormatter

class CloseRunStreamFilesets(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """MERGE INTO wmbs_fileset a
                 USING (
                   SELECT run_stream_fileset_assoc.run_id AS run_id,
                          run_stream_fileset_assoc.stream_id AS stream_id,
                          run_stream_fileset_assoc.fileset AS fileset
                   FROM run_stream_fileset_assoc
                   INNER JOIN wmbs_fileset ON
                     wmbs_fileset.id = run_stream_fileset_assoc.fileset AND
                     wmbs_fileset.open = 1
                   INNER JOIN run ON
                     run.run_id = run_stream_fileset_assoc.run_id AND
                     run.end_time > 0
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
                 ) b ON ( b.fileset = a.id )
                 WHEN MATCHED THEN UPDATE
                 SET a.open = 0,
                     a.last_update = :CLOSE_TIME
                 WHERE NOT EXISTS (
                   SELECT * FROM streamer
                   WHERE checkForZeroState(used) = 0
                   AND run_id = b.run_id
                   AND stream_id = b.stream_id
                 )
                 """

        binds = { 'CLOSE_TIME' : int(time.time()) }

        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)[0].fetchall()

        runs = []
        for result in results:
            runs.append(result[0])

        return runs
