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
               FROM wmbs_subscription sub
               WHERE sub.fileset = rr.fileset
                 AND sub.finished = 0
             )
             AND NOT EXISTS (
               SELECT 1
               FROM wmbs_subscription sub
               INNER JOIN wmbs_workflow wf ON wf.id = sub.workflow
               INNER JOIN dbsbuffer_workflow dbsw ON dbsw.name = wf.name
               INNER JOIN dbsbuffer_file df ON df.workflow = dbsw.id
               INNER JOIN dbsbuffer_file_runlumi_map rl ON rl.filename = df.id
               WHERE sub.fileset = rr.fileset
                 AND rl.run = rr.run_id
                 AND df.status != 'InDBS'
             )
             AND EXISTS (
               SELECT 1
               FROM wmbs_subscription sub
               INNER JOIN wmbs_workflow wf ON wf.id = sub.workflow
               INNER JOIN dbsbuffer_workflow dbsw ON dbsw.name = wf.name
               INNER JOIN dbsbuffer_file df ON df.workflow = dbsw.id
               INNER JOIN dbsbuffer_file_runlumi_map rl ON rl.filename = df.id
               WHERE sub.fileset = rr.fileset
                 AND rl.run = rr.run_id
             )
             GROUP BY rr.run_id,
                      rr.primds_id,
                      pd.name
             """


    def execute(self, conn = None, transaction = False):

        results = self.dbi.processData(self.sql, binds = {}, conn = conn,
                                       transaction = transaction)

        return self.formatDict(results)