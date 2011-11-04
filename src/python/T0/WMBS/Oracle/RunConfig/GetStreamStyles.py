"""
_GetStreamStyles_

Oracle implementation of GetStreamStyles

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetStreamStyles(DBFormatter):

    def execute(self, run, stream = None, conn = None, transaction = False):

        sqlStream = """"""
        if stream != None:
            sqlStream = """AND run_stream_style_assoc.stream_id =
                             (SELECT id FROM stream WHERE name = :STREAM)"""

        sql = """SELECT stream.name, processing_style.name
                 FROM run_stream_style_assoc
                 INNER JOIN stream ON
                   stream.id = run_stream_style_assoc.stream_id
                 INNER JOIN processing_style ON
                   processing_style.id = run_stream_style_assoc.style_id
                 WHERE run_stream_style_assoc.run_id = :RUN
                 %s """ % sqlStream

        binds = { 'RUN' : run }
        if stream != None:
            binds['STREAM'] = stream
        
        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)[0].fetchall()

        resultDict = {}
        for result in results:
            resultDict[result[0]] = result[1]

        return resultDict
