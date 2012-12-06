'''
_DeleteStreamers_

Oracle implementation of RunLumiCloseOut.DeleteStreamers

Created on Nov 30, 2012

@author: dballest
'''

from WMCore.Database.DBFormatter import DBFormatter

class DeleteStreamers(DBFormatter):
    """
    _DeleteStreamers_

    Delete the streamers with the given IDs from
    the streamer table
    """

    sql = """DELETE FROM streamer
             WHERE id = :FILEID
          """

    def execute(self, fileList, conn = None, transaction = False):
        """
        _execute_

        Executes the deletion
        """
        if not fileList:
            return
        binds = []
        for fileId in fileList:
            binds.append({"FILEID" : fileId})

        self.dbi.processData(self.sql, binds = binds, conn = conn,
                             transaction = transaction)

        return
