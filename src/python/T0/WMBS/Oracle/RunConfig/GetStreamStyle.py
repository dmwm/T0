"""
_GetStreamStyle_

Oracle implementation of GetStreamStyle

Return the processing style for a given run and stream.

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetStreamStyle(DBFormatter):

    def execute(self, run, stream, conn = None, transaction = False):

        sql = """SELECT processing_style.name
                 FROM run_stream_style_assoc
                 INNER JOIN processing_style ON
                   processing_style.id = run_stream_style_assoc.style_id
                 WHERE run_stream_style_assoc.run_id = :RUN
                 AND run_stream_style_assoc.stream_id =
                   (SELECT id FROM stream WHERE name = :STREAM)
                 """

        binds = { 'RUN' : run,
                  'STREAM' : stream }

        result = self.dbi.processData(sql, binds, conn = conn,
                                      transaction = transaction)[0].fetchall()[0][0]

        return result
