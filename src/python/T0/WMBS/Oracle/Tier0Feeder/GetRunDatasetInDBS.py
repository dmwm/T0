"""
_GetRunDatasetInDBS_

Oracle implementation of GetRunDatasetInDBS

Returns run/primds combinations where all files are uploaded to DBS

Checks all workflows associated with each primary dataset, including merge workflows

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetRunDatasetInDBS(DBFormatter):

    sql = """SELECT rr.run_id AS run,
                    rr.primds_id AS primds_id,
                    pd.name AS primds
             FROM reco_release_config rr
             INNER JOIN primary_dataset pd ON
               pd.id = rr.primds_id
             WHERE rr.in_datasvc = 3
             AND NOT EXISTS (
               SELECT 1
               FROM dbsbuffer_file df
               INNER JOIN dbsbuffer_file_runlumi_map rl ON 
                 rl.filename = df.id
               WHERE rl.run = rr.run_id
                 AND df.status != 'InDBS'
                 AND EXISTS (
                   SELECT 1
                   FROM dbsbuffer_workflow dbsw
                   WHERE dbsw.id = df.workflow
                     AND dbsw.name LIKE '%' || pd.name || '%'
                 )
             )
             AND EXISTS (
               SELECT 1
               FROM dbsbuffer_file df
               INNER JOIN dbsbuffer_file_runlumi_map rl ON 
                 rl.filename = df.id
               WHERE rl.run = rr.run_id
                 AND EXISTS (
                   SELECT 1
                   FROM dbsbuffer_workflow dbsw
                   WHERE dbsw.id = df.workflow
                     AND dbsw.name LIKE '%' || pd.name || '%'
                 )
             )
             GROUP BY rr.run_id,
                      rr.primds_id,
                      pd.name
             """

    def execute(self, conn = None, transaction = False):

        results = self.dbi.processData(self.sql, binds = {}, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)