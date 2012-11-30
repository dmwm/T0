"""
_CheckEndOfRunRecords_

Oracle implementation of WMBS.RunLumiCloseout.CheckEndOfRunRecords

Created on Nov 28, 2012

@author: dballest
"""

from WMCore.Database.DBFormatter import DBFormatter

class CheckEndOfRunRecords(DBFormatter):
    """
    _CheckEndOfRunRecords_

    Checks the CMS StorageManager database for
    End of Run records from the different instances
    """

    sql = """
          SELECT smdb.instance, smdb.status, smdb.n_instances
                 FROM CMS_STOMGR.runs smdb
                 WHERE smdb.runnumber = :RUN_ID
          """

    def execute(self, run, conn = None, transaction = False):
        """
        _execute_

        Execute the query, a dictionary with the following format
        {totalInstances : <int>,
         instancesWithEoR : [<str>, <str>],
         instancesWithoutEoR : [<str>, <str>]
        }
        """

        result = self.dbi.processData(self.sql, {'RUN_ID' : run}, conn = conn,
                                       transaction = transaction)

        resultDict = self.formatDict(result)

        formattedResult = {"totalInstances" : 0,
                           "instancesWithEoR" : [],
                           "instancesWithoutEoR" : []
                           }

        for entry in resultDict:
            formattedResult["totalInstances"] = max(entry["n_instances"], formattedResult["totalInstances"])
            if entry["status"] != 0:
                formattedResult["instancesWithoutEoR"].append(entry["instance"])
            else:
                formattedResult["instancesWithEoR"].append(entry["instance"])

        return formattedResult
