"""
_GetStreamDatasetTriggers_

Oracle implementation of GetStreamDatasetTriggers

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetStreamDatasetTriggers(DBFormatter):

    def execute(self, run, stream = None, conn = None, transaction = False):

        sqlStream = """"""
        if stream != None:
            sqlStream = """AND run_primds_stream_assoc.stream_id =
                             (SELECT id FROM stream WHERE name = :STREAM)"""

        sql = """SELECT stream.name, primary_dataset.name, trigger_label.name
                 FROM run_primds_stream_assoc
                 INNER JOIN run_trig_primds_assoc ON
                   run_trig_primds_assoc.run_id = run_primds_stream_assoc.run_id AND
                   run_trig_primds_assoc.primds_id = run_primds_stream_assoc.primds_id
                 INNER JOIN stream ON
                   stream.id = run_primds_stream_assoc.stream_id
                 INNER JOIN primary_dataset ON
                   primary_dataset.id = run_primds_stream_assoc.primds_id
                 INNER JOIN trigger_label ON
                    trigger_label.id = run_trig_primds_assoc.trig_id
                 WHERE run_primds_stream_assoc.run_id = :RUN
                 %s """ % sqlStream

        binds = { 'RUN' : run }
        if stream != None:
            binds['STREAM'] = stream
        
        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)[0].fetchall()

        resultDict = {}
        for result in results:

            stream = result[0]
            primds = result[1]
            trig = result[2]

            if not resultDict.has_key(stream):
                resultDict[stream] = {}
            if not resultDict[stream].has_key(primds):
                resultDict[stream][primds] = []

            resultDict[stream][primds].append(trig)

        return resultDict
