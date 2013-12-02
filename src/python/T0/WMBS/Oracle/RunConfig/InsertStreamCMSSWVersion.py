"""
_InsertStreamCMSSWVersion_

Oracle implementation of InsertStreamCMSSWVersion

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertStreamCMSSWVersion(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO run_stream_cmssw_assoc
                 (RUN_ID, STREAM_ID, ONLINE_VERSION)
                 SELECT :RUN,
                        (SELECT id FROM stream WHERE name = :STREAM),
                        id
                 FROM cmssw_version
                 WHERE name = :VERSION
                 AND NOT EXISTS (
                   SELECT *
                   FROM run_stream_cmssw_assoc
                   WHERE run_id = :RUN
                   AND id = (SELECT id FROM stream WHERE name = :STREAM)
                 )"""

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
