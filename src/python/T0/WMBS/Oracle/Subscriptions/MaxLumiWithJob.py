"""
_MaxLumiWithJob_

Oracle implementation of MaxLumiWithJob

Finds the highest lumi for all files associated
to jobs belonging to a subscription
"""

from WMCore.Database.DBFormatter import DBFormatter

class MaxLumiWithJob(DBFormatter):

    def execute(self, subscription, conn = None, transaction = False):

        sql = """SELECT MAX(wmbs_file_runlumi_map.lumi) as max_lumi
                 FROM wmbs_jobgroup
                 INNER JOIN wmbs_job ON
                   wmbs_job.jobgroup = wmbs_jobgroup.id
                 INNER JOIN wmbs_job_assoc ON
                   wmbs_job_assoc.job = wmbs_job.id
                 INNER JOIN wmbs_file_runlumi_map ON
                   wmbs_file_runlumi_map.fileid = wmbs_job_assoc.fileid
                 WHERE wmbs_jobgroup.subscription = :subscription
                 """

        results = self.dbi.processData(sql, { 'subscription' : subscription },
                                       conn = conn, transaction = transaction)

        for result in self.formatDict(results):
            return result['max_lumi']

        return 0
