#!/usr/bin/env python
"""
_Express_t_

Express job splitting test

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

        self.testWorkflow = Workflow(spec = "spec.xml", owner = "mnorman", name = "wf001", task="Test")
        self.testWorkflow.create()

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

        insertStreamDAO = daoFactory(classname = "RunConfig.InsertStream")
        insertStreamDAO.execute(binds = { 'STREAM' : "A" },
                                transaction = False)

        # keep for later
        self.insertStreamFilesetDAO = daoFactory(classname = "RunConfig.InsertStreamFileset")
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
        Test event threshold (single job creation)

        """
        self.insertStreamFilesetDAO.execute(1, "A", "TestFileset1")

        fileset1 = Fileset(name = "TestFileset1")
        fileset1.load()

        for i in range(2):
            newFile = File(makeUUID(), size = 1000, events = 100)
            newFile.addRun(Run(1, *[1]))
            newFile.setLocation("SomeSE", immediateSave = False)
            newFile.create()
            fileset1.addFile(newFile)
        fileset1.commit()

        subscription1  = Subscription(fileset = fileset1,
                                      workflow = self.testWorkflow,
                                      split_algo = "Express",
                                      type = "Express")
        subscription1.create()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = subscription1)

        jobGroups = jobFactory(maxInputEvents = 200)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup.")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create a single job.")

        job = jobGroups[0].jobs.pop()
        self.assertTrue(job['name'].startswith("Express-"),
                        "ERROR: Job has wrong name.")

        splitLumis = self.getSplitLumisDAO.execute()
        self.assertEqual(len(splitLumis), 0,
                         "ERROR: Split lumis were created.")

        return

    def test01(self):
        """
        _test01_

        Test event threshold (multiple job creation)

        """
        self.insertStreamFilesetDAO.execute(1, "A", "TestFileset1")

        fileset1 = Fileset(name = "TestFileset1")
        fileset1.load()

        for i in range(2):
            newFile = File(makeUUID(), size = 1000, events = 100)
            newFile.addRun(Run(1, *[1]))
            newFile.setLocation("SomeSE", immediateSave = False)
            newFile.create()
            fileset1.addFile(newFile)
        fileset1.commit()

        subscription1  = Subscription(fileset = fileset1,
                                      workflow = self.testWorkflow,
                                      split_algo = "Express",
                                      type = "Express")
        subscription1.create()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = subscription1)

        jobGroups = jobFactory(maxInputEvents = 199)

        self.assertEqual(len(jobGroups[0].jobs), 2,
                         "ERROR: JobFactory didn't create two jobs.")

        splitLumis = self.getSplitLumisDAO.execute()
        self.assertEqual(len(splitLumis), 1,
                         "ERROR: Didn't create a single split lumi.")

        return

    def test02(self):
        """
        _test02_

        Test multi lumis

        """
        self.insertStreamFilesetDAO.execute(1, "A", "TestFileset1")

        fileset1 = Fileset(name = "TestFileset1")
        fileset1.load()

        for i in range(2):
            newFile = File(makeUUID(), size = 1000, events = 100)
            newFile.addRun(Run(1, *[1+i]))
            newFile.setLocation("SomeSE", immediateSave = False)
            newFile.create()
            fileset1.addFile(newFile)
        fileset1.commit()

        subscription1  = Subscription(fileset = fileset1,
                                      workflow = self.testWorkflow,
                                      split_algo = "Express",
                                      type = "Express")
        subscription1.create()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = subscription1)

        jobGroups = jobFactory(maxInputEvents = 100)

        self.assertEqual(len(jobGroups[0].jobs), 2,
                         "ERROR: JobFactory didn't create two jobs.")

        splitLumis = self.getSplitLumisDAO.execute()
        self.assertEqual(len(splitLumis), 0,
                         "ERROR: Split lumis were created.")

        return

if __name__ == '__main__':
    unittest.main()
