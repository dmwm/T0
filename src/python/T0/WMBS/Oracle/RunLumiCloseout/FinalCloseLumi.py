"""
_FinalCloseLumi_

Oracle implementation of FinalCloseLumi

Check all not yet closed run/stream/lumis for complete file
counts and close them if all files are present.

"""

from WMCore.Database.DBFormatter import DBFormatter

class FinalCloseLumi(DBFormatter):

    def execute(self, currentTime, conn = None, transaction = False):

        sql = """MERGE INTO lumi_section_closed a
                 USING (
                   SELECT lumi_section_closed.run_id,
                          lumi_section_closed.stream_id,
                          lumi_section_closed.lumi_id
                   FROM lumi_section_closed
                   INNER JOIN streamer ON
                     streamer.run_id = lumi_section_closed.run_id AND
                     streamer.stream_id = lumi_section_closed.stream_id AND
                     streamer.lumi_id = lumi_section_closed.lumi_id
                   WHERE checkForZeroState(lumi_section_closed.close_time) = 0
                   GROUP BY lumi_section_closed.run_id,
                            lumi_section_closed.stream_id,
                            lumi_section_closed.lumi_id
                   HAVING COUNT(*) = MAX(lumi_section_closed.filecount)
                 ) b ON ( b.run_id = a.run_id AND
                          b.stream_id = a.stream_id AND
                          b.lumi_id = a.lumi_id )
                 WHEN MATCHED THEN UPDATE
                 SET a.close_time = :CLOSE_TIME
                 """

        binds = { 'CLOSE_TIME' : currentTime }

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
