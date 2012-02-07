"""
_InsertClosedLumi_

Oracle implementation of InsertClosedLumi

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertClosedLumi(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO lumi_section_closed
                 (RUN_ID, LUMI_ID, STREAM_ID, FILECOUNT, INSERT_TIME, CLOSE_TIME)
                 SELECT :RUN,
                        :LUMI,
                        stream.id,
                        :FILECOUNT,
                        :INSERT_TIME,
                        :CLOSE_TIME
                 FROM stream
                 WHERE stream.name = :STREAM
                 AND NOT EXISTS (
                   SELECT * FROM lumi_section_closed
                   WHERE run_id = :RUN
                   AND lumi_id = :LUMI
                   AND stream_id = stream.id
                 )"""

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
