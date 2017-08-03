"""
_GetRunDatasetDone_

Oracle implementation of GetRunDatasetDone

Returns run/primds combinations that are fully processed

Two queries since if we don't run PromptReco for a dataset,
'fully processed' is equivalent to PromptReco release.

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetRunDatasetDone(DBFormatter):

    sqlNoReco = """SELECT reco_release_config.run_id AS run,
                          reco_release_config.primds_id AS primds_id,
                          primary_dataset.name AS primds
                   FROM reco_release_config
                   INNER JOIN primary_dataset ON
                     primary_dataset.id = reco_release_config.primds_id
                   INNER JOIN reco_config ON
                     reco_config.run_id = reco_release_config.run_id AND
                     reco_config.primds_id = reco_release_config.primds_id AND
                     reco_config.do_reco = 0
                   WHERE checkForZeroOneTwoState(reco_release_config.in_datasvc) = 2
                   GROUP BY reco_release_config.run_id,
                            reco_release_config.primds_id,
                            primary_dataset.name
                   """

    sqlReco = """SELECT reco_release_config.run_id AS run,
                        reco_release_config.primds_id AS primds_id,
                        primary_dataset.name AS primds
                 FROM reco_release_config
                 INNER JOIN primary_dataset ON
                   primary_dataset.id = reco_release_config.primds_id
                 INNER JOIN wmbs_subscription ON
                   wmbs_subscription.fileset = reco_release_config.fileset
                 INNER JOIN wmbs_workflow ON
                   wmbs_workflow.id = wmbs_subscription.workflow
                 INNER JOIN wmbs_workflow runprimds_workflow ON
                   runprimds_workflow.name = wmbs_workflow.name
                 INNER JOIN wmbs_subscription runprimds_subscription ON
                   runprimds_subscription.workflow = runprimds_workflow.id
                 WHERE checkForZeroOneTwoState(reco_release_config.in_datasvc) = 2
                 GROUP BY reco_release_config.run_id,
                          reco_release_config.primds_id,
                          primary_dataset.name
                 HAVING SUM(runprimds_subscription.finished) = COUNT(*)
                 """

    def execute(self, conn = None, transaction = False):


        results = self.dbi.processData(self.sqlNoReco, binds = {}, conn = conn,
                                       transaction = transaction)

        returnList = self.formatDict(results)

        results = self.dbi.processData(self.sqlReco, binds = {}, conn = conn,
                                       transaction = transaction)

        returnList.extend(self.formatDict(results))

        return returnList
