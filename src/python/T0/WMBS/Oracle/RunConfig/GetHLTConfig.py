"""
_GetHLTConfig_

Oracle implementation of GetHLTConfig

Returns HLT configuration (process name and stream
to dataset to trigger mapping) for a given HLT key.

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetHLTConfig(DBFormatter):

    def execute(self, hltkey, conn = None, transaction = False):

        sql = """SELECT distinct a.name AS stream,   
                                 b.name AS dataset,   
                                 c.name AS path,   
                                 d.processname AS process   
                       FROM cms_hlt_gdr.u_streams a,   
                            cms_hlt_gdr.u_datasets b,   
                            cms_hlt_gdr.u_paths c,   
                            cms_hlt_gdr.u_confversions d,   
                            cms_hlt_gdr.u_pathid2strdst e,   
                            cms_hlt_gdr.u_streamids f,   
                            cms_hlt_gdr.u_datasetids g,   
                            cms_hlt_gdr.u_pathids h,   
                            cms_hlt_gdr.u_pathid2conf i,   
                            cms_hlt_gdr.u_conf2strdst j 
                       WHERE d.name = :HLTKEY  
                       AND i.id_confver = d.id   
                       AND h.id = i.id_pathid   
                       AND c.id = h.id_path   
                       AND e.id_pathid = h.id   
                       AND f.id = e.id_streamid   
                       AND f.fractodisk > 0   
                       AND a.id = f.id_stream   
                       AND g.id = e.id_datasetid   
                       AND b.id = g.id_dataset  
                       AND j.id_confver=d.id 
                       AND j.id_streamid= e.id_streamid 
                       AND j.id_datasetid= e.id_datasetid 
                       ORDER BY stream, dataset, path
                 """

#        sql = """SELECT d.streamlabel AS stream,
#                        c.datasetLabel AS dataset,
#                        b.name AS path,
#                        h.processname AS process
#                 FROM PathStreamDatasetAssoc a 
#                 INNER Join Paths b
#                 ON a.pathID = b.pathID
#                 INNER JOIN PrimaryDatasets c
#                 ON a.datasetID = c.datasetID
#                 INNER JOIN Streams d 
#                 ON a.streamId = d.streamID
#                 INNER JOIN ECStreamAssoc  e
#                 ON d.streamid = e.STREAMID
#                 INNER JOIN EventContents f
#                 ON e.eventContentId = f.eventContentId
#                 INNER JOIN ConfigurationContentAssoc g 
#                 ON g.eventContentId = f.eventContentId
#                 INNER JOIN Configurations h
#                 ON g.configID = h.configID
#                 WHERE h.configdescriptor = :HLTKEY
#                 AND d.fracToDisk > 0
#                 """

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

            if stream not in streamDict:
                streamDict[stream] = {}
            if dataset not in streamDict[stream]:
                streamDict[stream][dataset] = set([])
            streamDict[stream][dataset].add(path)

        return { 'mapping' : streamDict,
                 'process' : process }
