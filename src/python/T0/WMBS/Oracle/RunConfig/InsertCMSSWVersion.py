"""
_InsertCMSSWVersion_

Oracle implementation of InsertCMSSWVersion

"""

from WMCore.Database.DBFormatter import DBFormatter

class InsertCMSSWVersion(DBFormatter):

    def execute(self, binds, conn = None, transaction = False):

        sql = """DECLARE
                   cnt NUMBER(1);
                 BEGIN
                   SELECT COUNT(*)
                   INTO cnt
                   FROM cmssw_version
                   WHERE name = :VERSION
                   ;
                   IF (cnt = 0)
                   THEN
                     INSERT INTO cmssw_version
                     (ID, NAME)
                     VALUES(cmssw_version_SEQ.nextval, :VERSION)
                     ;
                   END IF;
                 EXCEPTION
                   WHEN DUP_VAL_ON_INDEX THEN NULL;
                 END;
                 """

        self.dbi.processData(sql, binds, conn = conn,
                             transaction = transaction)

        return
