#!/usr/bin/env python
"""
_Conditions_t_

Condition job splitting test

"""

import unittest
import threading
import logging
import time

from WMCore.WMBS.File import File
from WMCore.WMBS.Fileset import Fileset
from WMCore.WMBS.Subscription import Subscription
from WMCore.WMBS.Workflow import Workflow
from WMCore.DataStructs.Run import Run

from WMCore.DAOFactory import DAOFactory
from WMCore.JobSplitting.SplitterFactory import SplitterFactory
from WMQuality.TestInit import TestInit


class ConditionTest(unittest.TestCase):
    """
    _ExpressTest_

    Test for Express job splitter
    """

    def setUp(self):
        """
        _setUp_

        """
        import WMQuality.TestInit
        WMQuality.TestInit.deleteDatabaseAfterEveryTest("I'm Serious")

        self.testInit = TestInit(__file__)
        self.testInit.setLogging()
        self.testInit.setDatabaseConnection()

        self.testInit.setSchema(customModules = ["WMComponent.DBS3Buffer", "T0.WMBS"])

        self.splitterFactory = SplitterFactory(package = "T0.JobSplitting")

        myThread = threading.currentThread()
        daoFactory = DAOFactory(package = "T0.WMBS",
                                logger = logging,
                                dbinterface = myThread.dbi)

        wmbsDaoFactory = DAOFactory(package = "WMCore.WMBS",
                                    logger = logging,
                                    dbinterface = myThread.dbi)

        myThread.dbi.processData("""INSERT INTO wmbs_location
                                    (id, site_name, state, state_time)
                                    VALUES (1, 'SomeSite', 1, 1)
                                    """, transaction = False)
        
        myThread.dbi.processData("""INSERT INTO wmbs_pnns
                                    (id, pnn) 
                                    VALUES (1, 'SomePNN')
                                    """, transaction = False)

        myThread.dbi.processData("""INSERT INTO wmbs_location_pnns
                                    (location, pnn)
                                    VALUES (1, 1)
                                    """, transaction = False)

        insertRunDAO = daoFactory(classname = "RunConfig.InsertRun")
        insertRunDAO.execute(binds = { 'RUN' : 1,
                                       'HLTKEY' : "someHLTKey" },
                             transaction = False)

        insertLumiDAO = daoFactory(classname = "RunConfig.InsertLumiSection")
        insertLumiDAO.execute(binds = { 'RUN' : 1,
                                        'LUMI' : 1 },
                              transaction = False)

        insertStreamDAO = daoFactory(classname = "RunConfig.InsertStream")
        insertStreamDAO.execute(binds = { 'STREAM' : "Express" },
                                transaction = False)

        insertStreamFilesetDAO = daoFactory(classname = "RunConfig.InsertStreamFileset")
        insertStreamFilesetDAO.execute(1, "Express", "TestFileset1")

        insertStreamerDAO = daoFactory(classname = "RunConfig.InsertStreamer")
        insertStreamerDAO.execute(streamerPNN = "SomePNN",
                                  binds = { 'RUN' : 1,
                                            'P5_ID' : 1,
                                            'LUMI' : 1,
                                            'STREAM' : "Express",
                                            'TIME' : int(time.time()),
                                            'LFN' : "/streamer",
                                            'FILESIZE' : 0,
                                            'EVENTS' : 0 },
                                  transaction = False)

        insertPromptCalibrationDAO = daoFactory(classname = "RunConfig.InsertPromptCalibration")
        insertPromptCalibrationDAO.execute( { 'RUN' : 1,
                                              'STREAM' : "Express",
                                              'NUM_PRODUCER' : 1},
                                            transaction = False)

        self.completeFilesDAO = wmbsDaoFactory(classname = "Subscriptions.CompleteFiles")
        self.markPromptCalibrationFinishedDAO = daoFactory(classname = "ConditionUpload.MarkPromptCalibrationFinished")
        
        self.fileset1 = Fileset(name = "TestFileset1")
        self.fileset1.create()

        workflow1 = Workflow(spec = "spec.xml", owner = "hufnagel", name = "TestWorkflow1", task="Test")
        workflow1.create()

        self.subscription1  = Subscription(fileset = self.fileset1,
                                           workflow = workflow1,
                                           split_algo = "Condition",
                                           type = "Condition")
        self.subscription1.create()

        # set parentage chain and sqlite fileset
        alcaRecoFile = File("/alcareco", size = 0, events = 0)
        alcaRecoFile.addRun(Run(1, *[1]))
        alcaRecoFile.setLocation("SomePNN", immediateSave = False)
        alcaRecoFile.create()
        alcaPromptFile = File("/alcaprompt", size = 0, events = 0)
        alcaPromptFile.addRun(Run(1, *[1]))
        alcaPromptFile.setLocation("SomePNN", immediateSave = False)
        alcaPromptFile.create()
        sqliteFile = File("/sqlite", size = 0, events = 0)
        sqliteFile.create()
        self.fileset1.addFile(sqliteFile)
        self.fileset1.commit()

        results = myThread.dbi.processData("""SELECT lfn FROM wmbs_file_details
                                              """,
                                           transaction = False)[0].fetchall()

        setParentageDAO = wmbsDaoFactory(classname = "Files.SetParentage")
        setParentageDAO.execute(binds = [ { 'parent' : "/streamer",
                                            'child' : "/alcareco" },
                                          { 'parent' : "/alcareco",
                                            'child' : "/alcaprompt" },
                                          { 'parent' : "/alcaprompt",
                                            'child' : "/sqlite" } ],
                                transaction = False)

        # default split parameters
        self.splitArgs = {}
        self.splitArgs['runNumber'] = 1
        self.splitArgs['streamName'] = "Express"

        return

    def tearDown(self):
        """
        _tearDown_

        """
        self.testInit.clearDatabase()

        return

    def isPromptCalibFinished(self):
        """
        _isPromptCalibFinished_

        """
        myThread = threading.currentThread()

        result = myThread.dbi.processData("""SELECT finished
                                             FROM prompt_calib
                                             """,
                                          transaction = False)[0].fetchall()[0][0]

        return result

    def countPromptCalibFiles(self):
        """
        _deleteSplitLumis_

        """
        myThread = threading.currentThread()

        result = myThread.dbi.processData("""SELECT COUNT(*)
                                             FROM prompt_calib_file
                                             """,
                                          transaction = False)[0].fetchall()[0][0]

        return result

    def test00(self):
        """
        _test00_

        Make sure the job splitter behaves correctly.

        Just make sure the job splitter does nothing
        when the fileset is open and populates t0ast
        data structures when it's closed. In the later
        case all input files should be marked as
        acquired without creating a job as well.

        """
        mySplitArgs = self.splitArgs.copy()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription1)

        self.assertEqual(self.isPromptCalibFinished(), 0,
                         "ERROR: prompt_calib should not be finished")

        self.assertEqual(self.countPromptCalibFiles(), 0,
                         "ERROR: there should be no prompt_calib_file")

        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(self.isPromptCalibFinished(), 0,
                         "ERROR: prompt_calib should not be finished")

        self.assertEqual(self.countPromptCalibFiles(), 1,
                         "ERROR: there should be one prompt_calib_file")

        self.completeFilesDAO.execute(1, 4, transaction = False)
        self.markPromptCalibrationFinishedDAO.execute(1, 1, transaction = False)
        
        self.fileset1.markOpen(False)

        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup")

        self.assertEqual(self.isPromptCalibFinished(), 1,
                         "ERROR: prompt_calib should be finished")

        self.assertEqual(self.countPromptCalibFiles(), 1,
                         "ERROR: there should be one prompt_calib_file")

        return

if __name__ == '__main__':
    unittest.main()
