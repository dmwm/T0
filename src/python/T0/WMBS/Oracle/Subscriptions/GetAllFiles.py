"""
_GetAllFiles_

Oracle implementation of GetAllFiles

For a given subscription return all the
files in the corresponding fileset
"""

from WMCore.Database.DBFormatter import DBFormatter

class GetAllFiles(DBFormatter):

    sql = """SELECT wmbs_fileset_files.fileid AS id,
                    wmbs_file_details.lfn AS lfn,
                    wmbs_location_senames.se_name AS location
             FROM wmbs_subscription
             INNER JOIN wmbs_fileset_files ON
               wmbs_fileset_files.fileset = wmbs_subscription.fileset
             INNER JOIN wmbs_file_details ON
               wmbs_file_details.id = wmbs_fileset_files.fileid
             INNER JOIN wmbs_file_location ON
               wmbs_file_location.fileid = wmbs_fileset_files.fileid
             INNER JOIN wmbs_location ON
               wmbs_location.id = wmbs_file_location.location
             INNER JOIN wmbs_location_senames ON
               wmbs_location_senames.location = wmbs_location.id
             WHERE wmbs_subscription.id = :subscription
             """

    def execute(self, subscription, conn = None, transaction = False):

        results = self.dbi.processData(self.sql, { 'subscription' : subscription },
                                       conn = conn, transaction = transaction)

        ungroupedResults = self.formatDict(results)
        result = {}
        for entry in ungroupedResults:
            if entry['lfn'] not in result:
                entry['location'] = set([entry['location']])
                result[entry['lfn']] = entry
            else:
                result[entry['lfn']]['location'].add(entry['location'])

        return result.values()
