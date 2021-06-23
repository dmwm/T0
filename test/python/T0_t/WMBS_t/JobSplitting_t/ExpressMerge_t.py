#!/usr/bin/env python
"""
_ExpressMerge_t_
ExpressMerge job splitting test
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
from WMCore.Services.UUIDLib import makeUUID
from WMQuality.TestInit import TestInit


class ExpressMergeTest(unittest.TestCase):
    """
    _ExpressMergeTest_
    Test for ExpressMerge job splitter
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

        myThread.dbi.processData("""INSERT INTO wmbs_location
                                    (id, site_name, state, state_time)
                                    VALUES (1, 'SomeSite', 1, 1)
                                    """, transaction = False)
        myThread.dbi.processData("""INSERT INTO wmbs_pnns
                                    (id, pnn)
                                    VALUES (2, 'SomePNN')
                                    """, transaction = False)
        
        myThread.dbi.processData("""INSERT INTO wmbs_location_pnns
                                    (location, pnn)
                                    VALUES (1, 2)
                                    """, transaction = False)

        insertRunDAO = daoFactory(classname = "RunConfig.InsertRun")
        insertRunDAO.execute(binds = { 'RUN' : 1,
                                       'HLTKEY' : "someHLTKey" },
                             transaction = False)

        insertLumiDAO = daoFactory(classname = "RunConfig.InsertLumiSection")
        for lumi in range(1, 5):
            insertLumiDAO.execute(binds = { 'RUN' : 1,
                                            'LUMI' : lumi },
                                  transaction = False)

        insertStreamDAO = daoFactory(classname = "RunConfig.InsertStream")
        insertStreamDAO.execute(binds = { 'STREAM' : "Express" },
                                transaction = False)

        insertStreamFilesetDAO = daoFactory(classname = "RunConfig.InsertStreamFileset")
        insertStreamFilesetDAO.execute(1, "Express", "TestFileset1")

        fileset1 = Fileset(name = "TestFileset1")
        self.fileset2 = Fileset(name = "TestFileset2")
        fileset1.load()
        self.fileset2.create()

        workflow1 = Workflow(spec = "spec.xml", owner = "hufnagel", name = "TestWorkflow1", task="Test")
        workflow2 = Workflow(spec = "spec.xml", owner = "hufnagel", name = "TestWorkflow2", task="Test")
        workflow1.create()
        workflow2.create()

        self.subscription1  = Subscription(fileset = fileset1,
                                           workflow = workflow1,
                                           split_algo = "Express",
                                           type = "Express")
        self.subscription2  = Subscription(fileset = self.fileset2,
                                           workflow = workflow2,
                                           split_algo = "ExpressMerge",
                                           type = "ExpressMerge")
        self.subscription1.create()
        self.subscription2.create()

        myThread.dbi.processData("""INSERT INTO wmbs_workflow_output
                                    (WORKFLOW_ID, OUTPUT_IDENTIFIER, OUTPUT_FILESET)
                                    VALUES (%d, 'SOMEOUTPUT', %d)
                                    """ % (workflow1.id, self.fileset2.id),
                                 transaction = False)

        # keep for later
        self.insertSplitLumisDAO = daoFactory(classname = "JobSplitting.InsertSplitLumis")

        # default split parameters
        self.splitArgs = {}
        self.splitArgs['maxInputSize'] = 2 * 1024 * 1024 * 1024
        self.splitArgs['maxInputFiles'] = 500,
        self.splitArgs['maxLatency'] = 15 * 23

        return

    def tearDown(self):
        """
        _tearDown_
        """
        self.testInit.clearDatabase()

        return

    def deleteSplitLumis(self):
        """
        _deleteSplitLumis_
        """
        myThread = threading.currentThread()

        myThread.dbi.processData("""DELETE FROM lumi_section_split_active
                                    """,
                                 transaction = False)

        return

    def test00(self):
        """
        _test00_
        Test that the job name prefix feature works
        Test latency trigger (wait and 0)
        """
        mySplitArgs = self.splitArgs.copy()

        for lumi in [1]:
            for i in range(2):
                newFile = File(makeUUID(), size = 1000, events = 100)
                newFile.addRun(Run(1, *[lumi]))
                newFile.setLocation("SomePNN", immediateSave = False)
                newFile.create()
                self.fileset2.addFile(newFile)
        self.fileset2.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription2)

        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup")

        mySplitArgs['maxLatency'] = 0
        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create a single job")

        job = jobGroups[0].jobs[0]
        self.assertTrue(job['name'].startswith("ExpressMerge-"),
                        "ERROR: Job has wrong name")

        return

    def test01(self):
        """
        _test01_
        Test size and event triggers for single lumis (they are ignored)
        Test latency trigger (timed out)
        """
        mySplitArgs = self.splitArgs.copy()

        for lumi in [1]:
            for i in range(2):
                newFile = File(makeUUID(), size = 1000, events = 100)
                newFile.addRun(Run(1, *[lumi]))
                newFile.setLocation("SomePNN", immediateSave = False)
                newFile.create()
                self.fileset2.addFile(newFile)
        self.fileset2.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription2)

        mySplitArgs['maxInputSize'] = 1
        mySplitArgs['maxInputFiles'] = 1
        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup")

        time.sleep(1)

        mySplitArgs['maxLatency'] = 1
        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create a single job")

        return

    def test02(self):
        """
        _test02_
        Test input files threshold on multi lumis
        """
        mySplitArgs = self.splitArgs.copy()

        for lumi in [1, 2]:
            for i in range(2):
                newFile = File(makeUUID(), size = 1000, events = 100)
                newFile.addRun(Run(1, *[lumi]))
                newFile.setLocation("SomePNN", immediateSave = False)
                newFile.create()
                self.fileset2.addFile(newFile)
        self.fileset2.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription2)

        mySplitArgs['maxInputFiles'] = 1
        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup")

        time.sleep(1)

        mySplitArgs['maxLatency'] = 1
        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup")

        self.assertEqual(len(jobGroups[0].jobs), 2,
                         "ERROR: JobFactory didn't create two jobs")

        return

    def test03(self):
        """
        _test03_
        Test input size threshold on multi lumis
        """
        mySplitArgs = self.splitArgs.copy()

        for lumi in [1, 2]:
            for i in range(2):
                newFile = File(makeUUID(), size = 1000, events = 100)
                newFile.addRun(Run(1, *[lumi]))
                newFile.setLocation("SomePNN", immediateSave = False)
                newFile.create()
                self.fileset2.addFile(newFile)
        self.fileset2.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription2)

        mySplitArgs['maxInputSize'] = 1
        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup")

        time.sleep(1)

        mySplitArgs['maxLatency'] = 1
        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup")

        self.assertEqual(len(jobGroups[0].jobs), 2,
                         "ERROR: JobFactory didn't create two jobs")

        return

    def test04(self):
        """
        _test04_
        Test multi lumis express merges
        """
        mySplitArgs = self.splitArgs.copy()

        for lumi in [1, 2]:
            for i in range(2):
                newFile = File(makeUUID(), size = 1000, events = 100)
                newFile.addRun(Run(1, *[lumi]))
                newFile.setLocation("SomePNN", immediateSave = False)
                newFile.create()
                self.fileset2.addFile(newFile)
        self.fileset2.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription2)

        time.sleep(1)

        mySplitArgs['maxLatency'] = 1
        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create a single job")

        return

    def test05(self):
        """
        _test05_
        Test multi lumis express merges with holes
        """
        mySplitArgs = self.splitArgs.copy()

        for lumi in [1, 2, 4]:
            for i in range(2):
                newFile = File(makeUUID(), size = 1000, events = 100)
                newFile.addRun(Run(1, *[lumi]))
                newFile.setLocation("SomePNN", immediateSave = False)
                newFile.create()
                self.fileset2.addFile(newFile)
        self.fileset2.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription2)

        time.sleep(1)

        mySplitArgs['maxLatency'] = 1
        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup")

        self.assertEqual(len(jobGroups[0].jobs), 2,
                         "ERROR: JobFactory didn't create two jobs")

        return

    def test06(self):
        """
        _test06_
        Test active split lumis
        """
        mySplitArgs = self.splitArgs.copy()

        for lumi in [1]:
            for i in range(2):
                newFile = File(makeUUID(), size = 1000, events = 100)
                newFile.addRun(Run(1, *[lumi]))
                newFile.setLocation("SomePNN", immediateSave = False)
                newFile.create()
                self.fileset2.addFile(newFile)
        self.fileset2.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription2)

        self.insertSplitLumisDAO.execute( binds = { 'SUB' : self.subscription1['id'],
                                                    'LUMI' : 1 ,
                                                    'NFILES' : 5 } )

        mySplitArgs['maxLatency'] = 0
        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup")

        self.deleteSplitLumis()

        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create a single job")

        return

if __name__ == '__main__':
    unittest.main()
