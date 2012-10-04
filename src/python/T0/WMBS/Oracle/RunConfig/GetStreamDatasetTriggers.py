"""
_GetStreamDatasetTriggers_

Oracle implementation of GetStreamDatasetTriggers

Return primary dataset to trigger mapping for given run and stream

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetStreamDatasetTriggers(DBFormatter):

    def execute(self, run, stream, conn = None, transaction = False):

        sql = """SELECT primary_dataset.name, trigger_label.name
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
                 AND run_primds_stream_assoc.stream_id =
                   (SELECT id FROM stream WHERE name = :STREAM)
                 """

        binds = { 'RUN' : run,
                  'STREAM' : stream }
        
        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)[0].fetchall()

        resultDict = {}
        for result in results:

            primds = result[0]
            trig = result[1]

            if not resultDict.has_key(primds):
                resultDict[primds] = []

            resultDict[primds].append(trig)

        return resultDict
