"""
_GetHLTKeyForRun_

Oracle implementation of GetHLTKeyForRun

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetHLTKeyForRun(DBFormatter):

    def execute(self, run, conn = None, transaction = False):

        sql = """SELECT hltkey
                 FROM run
                 WHERE run_id = :RUN
                 """

        binds = { 'RUN' : run }
        
        hltkey = self.dbi.processData(sql, binds, conn = conn,
                                      transaction = transaction)[0].fetchall()[0][0]

        return hltkey
