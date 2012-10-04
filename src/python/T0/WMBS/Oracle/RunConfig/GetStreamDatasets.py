"""
_GetStreamDatasets_

Oracle implementation of GetStreamDatasets

Return list of primary datasets for given run and stream.
As we do not join to the stream to trigger assoc table,
this also returns error datasets.

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetStreamDatasets(DBFormatter):

    def execute(self, run, stream, conn = None, transaction = False):

        sql = """SELECT primary_dataset.name
                 FROM run_primds_stream_assoc
                 INNER JOIN primary_dataset ON
                   primary_dataset.id = run_primds_stream_assoc.primds_id
                 WHERE run_primds_stream_assoc.run_id = :RUN
                 AND run_primds_stream_assoc.stream_id = (SELECT id FROM stream WHERE name = :STREAM)
                 """

        binds = { 'RUN' : run,
                  'STREAM' : stream }
        
        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)[0].fetchall()

        datasets = set([])
        for result in results:
            datasets.add(result[0])

        return datasets
