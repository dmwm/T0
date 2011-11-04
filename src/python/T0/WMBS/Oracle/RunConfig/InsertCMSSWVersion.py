"""
_InsertCMSSWVersion_

Oracle implementation of InsertCMSSWVersion

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertCMSSWVersion(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """INSERT INTO cmssw_version
                 (ID, NAME)
                 SELECT cmssw_version_SEQ.nextval, :VERSION
                 FROM DUAL
                 WHERE NOT EXISTS (
                   SELECT * FROM cmssw_version WHERE NAME = :VERSION
                 )"""

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
