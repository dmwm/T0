"""
_ForceCloseLumi_

Oracle implementation of LumiRunCloseout.ForceCloseLumi

Created on Nov 30, 2012

@author: dballest
"""

import time

from WMCore.Database.DBFormatter import DBFormatter

class ForceCloseLumi(DBFormatter):
    """
    _ForceCloseLumi_

    Inserts a closing time for the given run,stream and lumi. If lumi
    doesn't exist then it's inserted into lumi_section_closed.
    Sets the filecount to 0 on those lumis.
    """

    sql = """MERGE INTO lumi_section_closed
             USING DUAL ON (
                            run_id = :RUN_ID AND
                            lumi_id = :LUMI_ID AND
                            stream_id = :STREAM_ID
                           )
             WHEN MATCHED THEN
                 UPDATE SET filecount = 0,
                            close_time = :CURRENT_TIME
             WHEN NOT MATCHED THEN
                 INSERT (run_id, lumi_id, stream_id, filecount, insert_time, close_time)
                 VALUES (:RUN_ID, :LUMI_ID, :STREAM_ID, 0, :CURRENT_TIME, :CURRENT_TIME)
          """

    def execute(self, run, streams, conn = None, transaction = False):
        """
        _execute_

        Executes the query, passes the current time
        """
        if not streams:
            return

        currentTime = int(time.time())

        binds = []
        for stream in streams:
            for lumi in streams[stream]:
                binds.append({"RUN_ID" : run,
                              "STREAM_ID" : stream,
                              "LUMI_ID" : lumi,
                              "CURRENT_TIME" : currentTime})

        self.dbi.processData(self.sql, binds = binds,
                             conn = conn,
                             transaction = transaction)

        return

