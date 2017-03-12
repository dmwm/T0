"""
_UpdateOfflineFileStatus_

Oracle implementation of UpdateOfflineFileStatus

"""

from WMCore.Database.DBFormatter import DBFormatter

class UpdateOfflineFileStatus(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """UPDATE file_transfer_status_offline
                 SET t0_repacked_time = CURRENT_TIMESTAMP,
                     repacked_retrieve = 1
                 WHERE p5_fileid = :P5_ID
                 AND t0_repacked_time IS NULL
                 AND repacked_retrieve is NULL
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
