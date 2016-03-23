"""
_FindRecoReleaseDatasets_

Oracle implementation of FindRecoReleaseDatasets

Return a list of datasets in any runs that wait
for PromptReco release.

"""

from WMCore.Database.DBFormatter import DBFormatter

class FindRecoReleaseDatasets(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT primary_dataset.name
                 FROM reco_release_config
                 INNER JOIN run ON
                   run.run_id = reco_release_config.run_id
                 INNER JOIN primary_dataset ON
                   primary_dataset.id = reco_release_config.primds_id
                 WHERE checkForZeroOneState(reco_release_config.released) = 0
                 AND run.stop_time > 0
                 GROUP BY primary_dataset.name
                 """

        results = self.dbi.processData(sql, binds = {}, conn = conn,
                                       transaction = transaction)[0].fetchall()

        datasets = []
        for result in results:
            datasets.append(result[0])

        return datasets
