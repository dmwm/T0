"""
_GetRepackConfig_

Oracle implementation of GetRepackConfig

Return Repack configuration for given run and stream.

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetRepackConfig(DBFormatter):

    def execute(self, run, stream, conn = None, transaction = False):

        sql = """SELECT repack_config.proc_version AS proc_ver,
                        cmssw_version.name AS cmssw
                 FROM repack_config
                 INNER JOIN run_stream_cmssw_assoc ON
                   run_stream_cmssw_assoc.run_id = repack_config.run_id AND
                   run_stream_cmssw_assoc.stream_id = repack_config.stream_id
                 INNER JOIN cmssw_version ON
                   cmssw_version.id = run_stream_cmssw_assoc.override_version
                 WHERE repack_config.run_id = :RUN
                 AND repack_config.stream_id = (SELECT id FROM stream WHERE name = :STREAM)
                 """

        binds = { 'RUN' : run,
                  'STREAM' : stream }
        
        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)[0]
