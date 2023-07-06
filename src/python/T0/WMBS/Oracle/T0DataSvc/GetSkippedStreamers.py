"""
_GetSkippedLumis_

Oracle implementation of GetSkippedLumis

Returns lumis that where skipped during job splitting

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetSkippedStreamers(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT st.id,
                       st.run_id, 
                       s.name, 
                       st.lumi_id, 
                       f.events 
                  FROM wmbs_sub_files_failed ff
                  JOIN wmbs_file_details f ON f.id = ff.fileid
                  JOIN streamer st ON st.id = f.id
                  JOIN stream s ON s.id = st.stream_id
                  WHERE st.skipped = 0
                 """

        results = self.dbi.processData(sql, binds = {}, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)
