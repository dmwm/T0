"""
_GetStreamOnlineVersion_

Oracle implementation of GetStreamOnlineVersion

Return online CMSSW version for a given run and stream.

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetStreamOnlineVersion(DBFormatter):

    def execute(self, run, stream, conn = None, transaction = False):

        sql = """SELECT cmssw_version.name
                 FROM run_stream_cmssw_assoc
                 INNER JOIN cmssw_version ON
                   cmssw_version.id = run_stream_cmssw_assoc.online_version
                 WHERE run_stream_cmssw_assoc.run_id = :RUN
                 AND run_stream_cmssw_assoc.stream_id = (SELECT id FROM stream WHERE name = :STREAM)
                 """

        binds = { 'RUN' : run,
                  'STREAM' : stream }
        
        onlineVersion = self.dbi.processData(sql, binds, conn = conn,
                                             transaction = transaction)[0].fetchall()[0][0]

        return onlineVersion
