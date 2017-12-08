"""
_GetPromptRecoStatus_

Oracle implementation of GetRecoStatus

Checks if PromptReco is enabled or disabled
(big red button controlled by ORM)

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetPromptRecoStatus(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT status
                 FROM promptreco_status
                 WHERE change_time =
                   (SELECT MAX(change_time) FROM promptreco_status)"""

        result = self.dbi.processData(sql, binds = {}, conn = conn,
                                      transaction = transaction)[0].fetchall()[0][0]

        return (result == 1)
