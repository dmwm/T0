#!/usr/bin/env python
"""
_Repack_t_

Repack job splitting test

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


class RepackTest(unittest.TestCase):
    """
    _RepackTest_

    Test for Repack job splitter
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

        self.fileset1 = Fileset(name = "TestFileset1")
        self.fileset1.load()

        workflow1 = Workflow(spec = "spec.xml", owner = "hufnagel", name = "TestWorkflow1", task="Test")
        workflow1.create()

        self.subscription1  = Subscription(fileset = self.fileset1,
                                           workflow = workflow1,
                                           split_algo = "Repack",
                                           type = "Repack")
        self.subscription1.create()

        # keep for later
        self.getSplitLumisDAO = daoFactory(classname = "JobSplitting.GetSplitLumis")

        return

    def tearDown(self):
        """
        _tearDown_

        """
        self.testInit.clearDatabase()

        return

    def test00(self):
        """
        _test00_

        Test that the job name prefix feature works
        Test multi lumi size threshold
        Multi lumi input

        """
        for i in range(8):
            newFile = File(makeUUID(), size = 1000, events = 100)
            newFile.addRun(Run(1, *[1 + i/2]))
            newFile.setLocation("SomeSE", immediateSave = False)
            newFile.create()
            self.fileset1.addFile(newFile)
        self.fileset1.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription1)

        jobGroups = jobFactory(maxStreamerSizeMultiLumi = 9000)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup.")

        jobGroups = jobFactory(maxStreamerSizeMultiLumi = 5000)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup.")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create a single job.")

        job = jobGroups[0].jobs[0]
        self.assertTrue(job['name'].startswith("Repack-"),
                        "ERROR: Job has wrong name.")

        self.assertEqual(len(job.getFiles()), 4,
                         "ERROR: Job does not process 4 files.")

        self.fileset1.markOpen(False)

        jobGroups = jobFactory(maxStreamerSizeMultiLumi = 5000)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup.")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create a single job.")

        job = jobGroups[0].jobs[0]
        self.assertTrue(job['name'].startswith("Repack-"),
                        "ERROR: Job has wrong name.")

        self.assertEqual(len(job.getFiles()), 4,
                         "ERROR: Job does not process 4 files.")

        splitLumis = self.getSplitLumisDAO.execute()
        self.assertEqual(len(splitLumis), 0,
                         "ERROR: Split lumis were created.")

        return

    def test01(self):
        """
        _test01_

        Test multi lumi event threshold
        Multi lumi input

        """
        for i in range(8):
            newFile = File(makeUUID(), size = 1000, events = 100)
            newFile.addRun(Run(1, *[1 + i/2]))
            newFile.setLocation("SomeSE", immediateSave = False)
            newFile.create()
            self.fileset1.addFile(newFile)
        self.fileset1.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription1)

        jobGroups = jobFactory(maxStreamerEventsMultiLumi = 900)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup.")

        jobGroups = jobFactory(maxStreamerEventsMultiLumi = 500)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup.")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create a single job.")

        job = jobGroups[0].jobs[0]
        self.assertEqual(len(job.getFiles()), 4,
                         "ERROR: Job does not process 4 files.")

        self.fileset1.markOpen(False)

        jobGroups = jobFactory(maxStreamerEventsMultiLumi = 500)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup.")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create a single job.")

        job = jobGroups[0].jobs[0]
        self.assertEqual(len(job.getFiles()), 4,
                         "ERROR: Job does not process 4 files.")

        splitLumis = self.getSplitLumisDAO.execute()
        self.assertEqual(len(splitLumis), 0,
                         "ERROR: Split lumis were created.")

        return

    def test02(self):
        """
        _test02_

        Test single lumi size threshold
        Single lumi input

        """
        for i in range(8):
            newFile = File(makeUUID(), size = 1000, events = 100)
            newFile.addRun(Run(1, *[1]))
            newFile.setLocation("SomeSE", immediateSave = False)
            newFile.create()
            self.fileset1.addFile(newFile)
        self.fileset1.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription1)

        jobGroups = jobFactory(maxStreamerSizeSingleLumi = 9000)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup.")

        jobGroups = jobFactory(maxStreamerSizeSingleLumi = 6500)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup.")

        self.assertEqual(len(jobGroups[0].jobs), 2,
                         "ERROR: JobFactory didn't create two jobs.")

        job = jobGroups[0].jobs[0]
        self.assertEqual(len(job.getFiles()), 6,
                         "ERROR: Job does not process 6 files.")

        job = jobGroups[0].jobs[1]
        self.assertEqual(len(job.getFiles()), 2,
                         "ERROR: Job does not process 2 files.")

        splitLumis = self.getSplitLumisDAO.execute()
        self.assertEqual(len(splitLumis), 1,
                         "ERROR: Split lumis were not created.")

        return

    def test03(self):
        """
        _test03_

        Test single lumi event threshold
        Single lumi input

        """
        for i in range(8):
            newFile = File(makeUUID(), size = 1000, events = 100)
            newFile.addRun(Run(1, *[1]))
            newFile.setLocation("SomeSE", immediateSave = False)
            newFile.create()
            self.fileset1.addFile(newFile)
        self.fileset1.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription1)

        jobGroups = jobFactory(maxStreamerEventsSingleLumi = 900)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup.")

        jobGroups = jobFactory(maxStreamerEventsSingleLumi = 650)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup.")

        self.assertEqual(len(jobGroups[0].jobs), 2,
                         "ERROR: JobFactory didn't create two jobs.")

        job = jobGroups[0].jobs[0]
        self.assertEqual(len(job.getFiles()), 6,
                         "ERROR: Job does not process 6 files.")

        job = jobGroups[0].jobs[1]
        self.assertEqual(len(job.getFiles()), 2,
                         "ERROR: Job does not process 2 files.")

        splitLumis = self.getSplitLumisDAO.execute()
        self.assertEqual(len(splitLumis), 1,
                         "ERROR: Split lumis were not created.")

        return

    def test04(self):
        """
        _test04_

        Test streamer count threshold (only multi lumi)
        Multi lumi input

        """
        for i in range(8):
            newFile = File(makeUUID(), size = 1000, events = 100)
            newFile.addRun(Run(1, *[1 + i/2]))
            newFile.setLocation("SomeSE", immediateSave = False)
            newFile.create()
            self.fileset1.addFile(newFile)
        self.fileset1.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription1)

        jobGroups = jobFactory(maxStreamerCount = 9)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup.")

        jobGroups = jobFactory(maxStreamerCount = 5)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup.")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create a single job.")

        job = jobGroups[0].jobs[0]
        self.assertEqual(len(job.getFiles()), 4,
                         "ERROR: Job does not process 4 files.")

        self.fileset1.markOpen(False)

        jobGroups = jobFactory(maxStreamerCount = 5)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup.")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create a single job.")

        job = jobGroups[0].jobs[0]
        self.assertEqual(len(job.getFiles()), 4,
                         "ERROR: Job does not process 4 files.")

        splitLumis = self.getSplitLumisDAO.execute()
        self.assertEqual(len(splitLumis), 0,
                         "ERROR: Split lumis were created.")

        return

    def test05(self):
        """
        _test05_

        Test repacking of multiple lumis with holes in the lumi sequence
        Multi lumi input

        """
        for i in range(2,4):
            newFile = File(makeUUID(), size = 1000, events = 100)
            newFile.addRun(Run(1, *[1 + i/2]))
            newFile.setLocation("SomeSE", immediateSave = False)
            newFile.create()
            self.fileset1.addFile(newFile)
        for i in range(6,8):
            newFile = File(makeUUID(), size = 1000, events = 100)
            newFile.addRun(Run(1, *[1 + i/2]))
            newFile.setLocation("SomeSE", immediateSave = False)
            newFile.create()
            self.fileset1.addFile(newFile)
        self.fileset1.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription1)

        jobGroups = jobFactory(maxStreamerCount = 3)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup.")

        return

if __name__ == '__main__':
    unittest.main()
