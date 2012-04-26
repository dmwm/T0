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

        insertStreamFilesetDAO = daoFactory(classname = "RunConfig.InsertStreamFileset")
        insertStreamFilesetDAO.execute(1, "A", "TestFileset1")

        self.fileset1 = Fileset(name = "TestFileset1")
        self.fileset1.load()

        workflow1 = Workflow(spec = "spec.xml", owner = "hufnagel", name = "TestWorkflow1", task="Test")
        workflow1.create()

        self.subscription1  = Subscription(fileset = self.fileset1,
                                           workflow = workflow1,
                                           split_algo = "Express",
                                           type = "Express")
        self.subscription1.create()

        return

    def tearDown(self):
        """
        _tearDown_

        """
        self.testInit.clearDatabase()

        return

    def getNumActiveSplitLumis(self):
        """
        _getNumActiveSplitLumis_

        helper function that counts the number of active split lumis
        """
        myThread = threading.currentThread()

        results = myThread.dbi.processData("""SELECT COUNT(*)
                                              FROM lumi_section_split_active
                                              """, transaction = False)[0].fetchall()

        return results[0][0]

    def test00(self):
        """
        _test00_

        Test that the job name prefix feature works
        Test event threshold (single job creation)

        """
        for i in range(2):
            newFile = File(makeUUID(), size = 1000, events = 100)
            newFile.addRun(Run(1, *[1]))
            newFile.setLocation("SomeSE", immediateSave = False)
            newFile.create()
            self.fileset1.addFile(newFile)
        self.fileset1.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription1)

        jobGroups = jobFactory(maxInputEvents = 200)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create a single job")

        job = jobGroups[0].jobs[0]
        self.assertTrue(job['name'].startswith("Express-"),
                        "ERROR: Job has wrong name")

        self.assertEqual(self.getNumActiveSplitLumis(), 0,
                         "ERROR: Split lumis were created")

        return

    def test01(self):
        """
        _test01_

        Test event threshold (multiple job creation)

        """
        for i in range(2):
            newFile = File(makeUUID(), size = 1000, events = 100)
            newFile.addRun(Run(1, *[1]))
            newFile.setLocation("SomeSE", immediateSave = False)
            newFile.create()
            self.fileset1.addFile(newFile)
        self.fileset1.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription1)

        jobGroups = jobFactory(maxInputEvents = 199)

        self.assertEqual(len(jobGroups[0].jobs), 2,
                         "ERROR: JobFactory didn't create two jobs")

        self.assertEqual(self.getNumActiveSplitLumis(), 1,
                         "ERROR: Didn't create a single split lumi")

        return

    def test02(self):
        """
        _test02_

        Test multi lumis

        """
        for i in range(2):
            newFile = File(makeUUID(), size = 1000, events = 100)
            newFile.addRun(Run(1, *[1+i]))
            newFile.setLocation("SomeSE", immediateSave = False)
            newFile.create()
            self.fileset1.addFile(newFile)
        self.fileset1.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription1)

        jobGroups = jobFactory(maxInputEvents = 100)

        self.assertEqual(len(jobGroups[0].jobs), 2,
                         "ERROR: JobFactory didn't create two jobs")

        self.assertEqual(self.getNumActiveSplitLumis(), 0,
                         "ERROR: Split lumis were created")

        return

if __name__ == '__main__':
    unittest.main()
