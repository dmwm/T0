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
from WMCore.Services.UUID import makeUUID
from WMQuality.TestInit import TestInit


class ExpressTest(unittest.TestCase):
    """
    _ExpressTest_

    Test for Express job splitter
    """

    def setUp(self):
        """
        _setUp_

        """
        self.testInit = TestInit(__file__)
        self.testInit.setLogging()
        self.testInit.setDatabaseConnection()

        self.testInit.setSchema(customModules = ["T0.WMBS"])

        self.splitterFactory = SplitterFactory(package = "T0.JobSplitting")

        myThread = threading.currentThread()
        daoFactory = DAOFactory(package = "T0.WMBS",
                                logger = logging,
                                dbinterface = myThread.dbi)

        myThread.dbi.processData("""INSERT INTO wmbs_location
                                    (id, site_name, se_name)
                                    VALUES (wmbs_location_SEQ.nextval, 'SomeSite', 'SomeSE')
                                    """, transaction = False)

        insertRunDAO = daoFactory(classname = "RunConfig.InsertRun")
        insertRunDAO.execute(binds = { 'RUN' : 1,
                                       'TIME' : int(time.time()),
                                       'HLTKEY' : "someHLTKey" },
                             transaction = False)

        insertLumiDAO = daoFactory(classname = "RunConfig.InsertLumiSection")
        insertLumiDAO.execute(binds = { 'RUN' : 1,
                                        'LUMI' : 1 },
                              transaction = False)
        insertLumiDAO.execute(binds = { 'RUN' : 1,
                                        'LUMI' : 2 },
                              transaction = False)
        insertLumiDAO.execute(binds = { 'RUN' : 1,
                                        'LUMI' : 3 },
                              transaction = False)
        insertLumiDAO.execute(binds = { 'RUN' : 1,
                                        'LUMI' : 4 },
                              transaction = False)

        insertStreamDAO = daoFactory(classname = "RunConfig.InsertStream")
        insertStreamDAO.execute(binds = { 'STREAM' : "A" },
                                transaction = False)

        insertStreamFilesetDAO = daoFactory(classname = "RunConfig.InsertStreamFileset")
        insertStreamFilesetDAO.execute(1, "A", "TestFileset1")

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
        for i in range(2):
            newFile = File(makeUUID(), size = 1000, events = 100)
            newFile.addRun(Run(1, *[1]))
            newFile.setLocation("SomeSE", immediateSave = False)
            newFile.create()
            self.fileset2.addFile(newFile)
        self.fileset2.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription2)

        jobGroups = jobFactory(maxInputSize = 2 * 1024 * 1024 * 1024,
                               maxInputFiles = 1000,
                               maxLatency = 3)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup.")

        jobGroups = jobFactory(maxInputSize = 2 * 1024 * 1024,
                               maxInputFiles = 1000,
                               maxLatency = 0)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup.")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create a single job.")

        job = jobGroups[0].jobs.pop()
        self.assertTrue(job['name'].startswith("ExpressMerge-"),
                        "ERROR: Job has wrong name.")

        return

    def test01(self):
        """
        _test01_

        Test size and event triggers for single lumis (they are ignored)
        Test latency trigger (timed out)

        """
        for i in range(2):
            newFile = File(makeUUID(), size = 1000, events = 100)
            newFile.addRun(Run(1, *[1]))
            newFile.setLocation("SomeSE", immediateSave = False)
            newFile.create()
            self.fileset2.addFile(newFile)
        self.fileset2.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription2)

        jobGroups = jobFactory(maxInputSize = 1,
                               maxInputFiles = 1,
                               maxLatency = 3)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup.")

        time.sleep(1)

        jobGroups = jobFactory(maxInputSize = 1,
                               maxInputFiles = 1,
                               maxLatency = 1)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup.")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create a single job.")

        return

    def test02(self):
        """
        _test02_

        Test input files threshold on multi lumis

        """
        for i in range(4):
            newFile = File(makeUUID(), size = 1000, events = 100)
            newFile.addRun(Run(1, *[1+i/2]))
            newFile.setLocation("SomeSE", immediateSave = False)
            newFile.create()
            self.fileset2.addFile(newFile)
        self.fileset2.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription2)

        jobGroups = jobFactory(maxInputSize = 2 * 1024 * 1024 * 1024,
                               maxInputFiles = 1,
                               maxLatency = 3)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup.")

        time.sleep(1)

        jobGroups = jobFactory(maxInputSize = 2 * 1024 * 1024 * 1024,
                               maxInputFiles = 1,
                               maxLatency = 1)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup.")

        self.assertEqual(len(jobGroups[0].jobs), 2,
                         "ERROR: JobFactory didn't create two jobs.")

        return

    def test03(self):
        """
        _test03_

        Test input size threshold on multi lumis

        """
        for i in range(4):
            newFile = File(makeUUID(), size = 1000, events = 100)
            newFile.addRun(Run(1, *[1+i/2]))
            newFile.setLocation("SomeSE", immediateSave = False)
            newFile.create()
            self.fileset2.addFile(newFile)
        self.fileset2.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription2)

        jobGroups = jobFactory(maxInputSize = 1,
                               maxInputFiles = 1000,
                               maxLatency = 3)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup.")

        time.sleep(1)

        jobGroups = jobFactory(maxInputSize = 1,
                               maxInputFiles = 1000,
                               maxLatency = 1)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup.")

        self.assertEqual(len(jobGroups[0].jobs), 2,
                         "ERROR: JobFactory didn't create two jobs.")

        return

    def test04(self):
        """
        _test04_

        Test multi lumis express merges

        """
        for i in range(4):
            newFile = File(makeUUID(), size = 1000, events = 100)
            newFile.addRun(Run(1, *[1+i/2]))
            newFile.setLocation("SomeSE", immediateSave = False)
            newFile.create()
            self.fileset2.addFile(newFile)
        self.fileset2.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription2)

        time.sleep(1)

        jobGroups = jobFactory(maxInputSize = 2 * 1024 * 1024 * 1024,
                               maxInputFiles = 1000,
                               maxLatency = 1)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup.")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create a single job.")

        return

    def test05(self):
        """
        _test05_

        Test multi lumis express merges with holes

        """
        for i in range(4):
            newFile = File(makeUUID(), size = 1000, events = 100)
            newFile.addRun(Run(1, *[1+i/2]))
            newFile.setLocation("SomeSE", immediateSave = False)
            newFile.create()
            self.fileset2.addFile(newFile)
        for i in range(6,8):
            newFile = File(makeUUID(), size = 1000, events = 100)
            newFile.addRun(Run(1, *[1+i/2]))
            newFile.setLocation("SomeSE", immediateSave = False)
            newFile.create()
            self.fileset2.addFile(newFile)
        self.fileset2.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription2)

        time.sleep(1)

        jobGroups = jobFactory(maxInputSize = 2 * 1024 * 1024 * 1024,
                               maxInputFiles = 1000,
                               maxLatency = 1)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup.")

        self.assertEqual(len(jobGroups[0].jobs), 2,
                         "ERROR: JobFactory didn't create two jobs.")

        return

    def test06(self):
        """
        _test06_

        Test active split lumis

        """
        for i in range(2):
            newFile = File(makeUUID(), size = 1000, events = 100)
            newFile.addRun(Run(1, *[1]))
            newFile.setLocation("SomeSE", immediateSave = False)
            newFile.create()
            self.fileset2.addFile(newFile)
        self.fileset2.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription2)

        self.insertSplitLumisDAO.execute( binds = { 'SUB' : self.subscription1['id'],
                                                    'LUMI' : 1 } )

        jobGroups = jobFactory(maxInputSize = 2 * 1024 * 1024 * 1024,
                               maxInputFiles = 1000,
                               maxLatency = 0)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup.")

        self.deleteSplitLumis()

        jobGroups = jobFactory(maxInputSize = 2 * 1024 * 1024 * 1024,
                               maxInputFiles = 1000,
                               maxLatency = 0)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup.")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create a single job.")

        return

if __name__ == '__main__':
    unittest.main()
