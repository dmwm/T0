"""
_Destroy_

Implementation of Destroy for Oracle

"""

import threading

from WMCore.Database.DBCreator import DBCreator

class Destroy(DBCreator):    

    def __init__(self, logger = None, dbi = None):
        """
        _init_

        Call the DBCreator constructor and delete the schema

        """
        myThread = threading.currentThread()
        if logger == None:
            logger = myThread.logger
        if dbi == None:
            dbi = myThread.dbi

        DBCreator.__init__(self, logger, dbi)

        allTables = [ "cmssw_version",
                      "stream",
                      "processing_style",
                      "run_status",
                      "run",
                      "lumi_section",
                      "lumi_section_closed",
                      "lumi_section_split_active",
                      "run_stream_primds_assoc",
                      "run_stream_cmssw_assoc",
                      "run_stream_style_assoc",
                      "run_stream_sub_assoc",
                      "streamer" ]

        for table in allTables:
            self.delete[table] = """DROP TABLE %s CASCADE CONSTRAINTS""" % table

        return

    def execute(self, conn = None, transaction = None):
        """
        _execute_

        """
        DBCreator.execute(self, conn, transaction)

        return True
