"""
_GetHLTConfig_

Oracle implementation of GetHLTConfig

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetHLTConfig(DBFormatter):

    def execute(self, hltkey, conn = None, transaction = False):

        sql = """SELECT d.streamlabel AS stream,
                        c.datasetLabel AS dataset,
                        b.name AS path,
                        h.processname AS process
                 FROM PathStreamDatasetAssoc a 
                 INNER Join Paths b
                 ON a.pathID = b.pathID
                 INNER JOIN PrimaryDatasets c
                 ON a.datasetID = c.datasetID
                 INNER JOIN Streams d 
                 ON a.streamId = d.streamID
                 INNER JOIN ECStreamAssoc  e
                 ON d.streamid = e.STREAMID
                 INNER JOIN EventContents f
                 ON e.eventContentId = f.eventContentId
                 INNER JOIN ConfigurationContentAssoc g 
                 ON g.eventContentId = f.eventContentId
                 INNER JOIN Configurations h
                 ON g.configID = h.configID
                 WHERE h.configdescriptor = :HLTKEY
                 AND d.fracToDisk > 0"""

        binds = { 'HLTKEY' : hltkey }

        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)

        streamDict = {}
        process = None

        for result in self.formatDict(results):

            stream = result['stream']
            dataset = result['dataset']
            path = result['path']
            process = result['process']

            if dataset == "VBF1Parked ":
                dataset = "VBF1Parked"

            if not streamDict.has_key(stream):
                streamDict[stream] = {}
            if not streamDict[stream].has_key(dataset):
                streamDict[stream][dataset] = set([])
            streamDict[stream][dataset].add(path)

        return { 'mapping' : streamDict,
                 'process' : process }
