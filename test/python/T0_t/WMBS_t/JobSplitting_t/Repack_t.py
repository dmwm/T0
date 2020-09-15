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
from WMCore.Services.UUIDLib import makeUUID
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
        for lumi in [1, 2, 3, 4]:
            insertLumiDAO.execute(binds = { 'RUN' : 1,
                                            'LUMI' : lumi },
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
        self.insertClosedLumiDAO = daoFactory(classname = "RunLumiCloseout.InsertClosedLumi")
        self.currentTime = int(time.time())

        # default split parameters
        self.splitArgs = {}
        self.splitArgs['maxSizeSingleLumi'] = 20*1024*1024*1024
        self.splitArgs['maxSizeMultiLumi'] = 10*1024*1024*1024
        self.splitArgs['maxInputEvents'] = 500000
        self.splitArgs['maxInputFiles'] = 1000
        self.splitArgs['maxLatency'] = 50000

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
        Test multi lumi size threshold
        Multi lumi input

        """
        mySplitArgs = self.splitArgs.copy()

        for lumi in [1, 2, 3, 4]:
            filecount = 2
            for i in range(filecount):
                newFile = File(makeUUID(), size = 1000, events = 100)
                newFile.addRun(Run(1, *[lumi]))
                newFile.setLocation("SomePNN", immediateSave = False)
                newFile.create()
                self.fileset1.addFile(newFile)

        self.fileset1.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription1)

        mySplitArgs['maxSizeMultiLumi'] = self.splitArgs['maxSizeMultiLumi']
        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup")

        mySplitArgs['maxSizeMultiLumi'] = 5000
        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create a single job")

        job = jobGroups[0].jobs[0]
        self.assertTrue(job['name'].startswith("Repack-"),
                        "ERROR: Job has wrong name")

        self.assertEqual(len(job.getFiles()), 4,
                         "ERROR: Job does not process 4 files")

        self.fileset1.markOpen(False)

        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create a single job")

        job = jobGroups[0].jobs[0]
        self.assertTrue(job['name'].startswith("Repack-"),
                        "ERROR: Job has wrong name")

        self.assertEqual(len(job.getFiles()), 4,
                         "ERROR: Job does not process 4 files")

        self.assertEqual(self.getNumActiveSplitLumis(), 0,
                         "ERROR: Split lumis were created")

        return

    def test01(self):
        """
        _test01_

        Test multi lumi event threshold
        Multi lumi input

        """
        mySplitArgs = self.splitArgs.copy()

        insertClosedLumiBinds = []
        for lumi in [1, 2, 3, 4]:
            filecount = 2
            for i in range(filecount):
                newFile = File(makeUUID(), size = 1000, events = 100)
                newFile.addRun(Run(1, *[lumi]))
                newFile.setLocation("SomePNN", immediateSave = False)
                newFile.create()
                self.fileset1.addFile(newFile)
                insertClosedLumiBinds.append( { 'RUN' : 1,
                                                'LUMI' : lumi,
                                                'STREAM' : "A",
                                                'FILECOUNT' : filecount,
                                                'INSERT_TIME' : self.currentTime,
                                                'CLOSE_TIME' : self.currentTime } )
        self.fileset1.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription1)

        self.insertClosedLumiDAO.execute(binds = insertClosedLumiBinds,
                                         transaction = False)

        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup")

	mySplitArgs['maxInputEvents'] = 500
        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create a single job")

        job = jobGroups[0].jobs[0]
        self.assertEqual(len(job.getFiles()), 4,
                         "ERROR: Job does not process 4 files")

        self.fileset1.markOpen(False)

        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create a single job")

        job = jobGroups[0].jobs[0]
        self.assertEqual(len(job.getFiles()), 4,
                         "ERROR: Job does not process 4 files")

        self.assertEqual(self.getNumActiveSplitLumis(), 0,
                         "ERROR: Split lumis were created")

        return

    def test02(self):
        """
        _test02_

        Test single lumi size threshold
        Single lumi input

        """
        mySplitArgs = self.splitArgs.copy()

        insertClosedLumiBinds = []
        for lumi in [1]:
            filecount = 8
            for i in range(filecount):
                newFile = File(makeUUID(), size = 1000, events = 100)
                newFile.addRun(Run(1, *[lumi]))
                newFile.setLocation("SomePNN", immediateSave = False)
                newFile.create()
                self.fileset1.addFile(newFile)
                insertClosedLumiBinds.append( { 'RUN' : 1,
                                                'LUMI' : lumi,
                                                'STREAM' : "A",
                                                'FILECOUNT' : filecount,
                                                'INSERT_TIME' : self.currentTime,
                                                'CLOSE_TIME' : self.currentTime } )
        self.fileset1.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription1)

        self.insertClosedLumiDAO.execute(binds = insertClosedLumiBinds,
                                         transaction = False)
        
        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup")

        mySplitArgs['maxSizeSingleLumi'] = 6500
        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup")

        self.assertEqual(len(jobGroups[0].jobs), 2,
                         "ERROR: JobFactory didn't create two jobs")

        job = jobGroups[0].jobs[0]
        self.assertEqual(len(job.getFiles()), 6,
                         "ERROR: Job does not process 6 files")

        job = jobGroups[0].jobs[1]
        self.assertEqual(len(job.getFiles()), 2,
                         "ERROR: Job does not process 2 files")

        self.assertEqual(self.getNumActiveSplitLumis(), 1,
                         "ERROR: Split lumis were not created")

        return

    def test03(self):
        """
        _test03_

        Test single lumi event threshold
        Single lumi input

        """
        mySplitArgs = self.splitArgs.copy()

        insertClosedLumiBinds = []
        for lumi in [1]:
            filecount = 8
            for i in range(filecount):
                newFile = File(makeUUID(), size = 1000, events = 100)
                newFile.addRun(Run(1, *[lumi]))
                newFile.setLocation("SomePNN", immediateSave = False)
                newFile.create()
                self.fileset1.addFile(newFile)
                insertClosedLumiBinds.append( { 'RUN' : 1,
                                                'LUMI' : lumi,
                                                'STREAM' : "A",
                                                'FILECOUNT' : filecount,
                                                'INSERT_TIME' : self.currentTime,
                                                'CLOSE_TIME' : self.currentTime } )
        self.fileset1.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription1)

        self.insertClosedLumiDAO.execute(binds = insertClosedLumiBinds,
                                         transaction = False)

	jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup")

        mySplitArgs['maxInputEvents'] = 650
        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup")

        self.assertEqual(len(jobGroups[0].jobs), 2,
                         "ERROR: JobFactory didn't create two jobs")

        job = jobGroups[0].jobs[0]
        self.assertEqual(len(job.getFiles()), 6,
                         "ERROR: Job does not process 6 files")

        job = jobGroups[0].jobs[1]
        self.assertEqual(len(job.getFiles()), 2,
                         "ERROR: Job does not process 2 files")

        self.assertEqual(self.getNumActiveSplitLumis(), 1,
                         "ERROR: Split lumis were not created")

        return

    def test04(self):
        """
        _test04_

        Test streamer count threshold (only multi lumi)
        Multi lumi input

        """
        mySplitArgs = self.splitArgs.copy()

        insertClosedLumiBinds = []
        for lumi in [1, 2, 3, 4]:
            filecount = 2
            for i in range(filecount):
                newFile = File(makeUUID(), size = 1000, events = 100)
                newFile.addRun(Run(1, *[lumi]))
                newFile.setLocation("SomePNN", immediateSave = False)
                newFile.create()
                self.fileset1.addFile(newFile)
                insertClosedLumiBinds.append( { 'RUN' : 1,
                                                'LUMI' : lumi,
                                                'STREAM' : "A",
                                                'FILECOUNT' : filecount,
                                                'INSERT_TIME' : self.currentTime,
                                                'CLOSE_TIME' : self.currentTime } )
        self.fileset1.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription1)

        self.insertClosedLumiDAO.execute(binds = insertClosedLumiBinds,
                                         transaction = False)

	jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup")

        mySplitArgs['maxInputFiles'] = 5
        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create a single job")

        job = jobGroups[0].jobs[0]
        self.assertEqual(len(job.getFiles()), 4,
                         "ERROR: Job does not process 4 files")

        self.fileset1.markOpen(False)

        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create a single job")

        job = jobGroups[0].jobs[0]
        self.assertEqual(len(job.getFiles()), 4,
                         "ERROR: Job does not process 4 files")

        self.assertEqual(self.getNumActiveSplitLumis(), 0,
                         "ERROR: Split lumis were created")

        return

    def test05(self):
        """
        _test05_

        Test repacking of multiple lumis with holes in the lumi sequence
        Multi lumi input

        """
        mySplitArgs = self.splitArgs.copy()

        insertClosedLumiBinds = []
        for lumi in [1, 2, 4]:
            filecount = 2
            for i in range(filecount):
                newFile = File(makeUUID(), size = 1000, events = 100)
                newFile.addRun(Run(1, *[lumi]))
                newFile.setLocation("SomePNN", immediateSave = False)
                newFile.create()
                self.fileset1.addFile(newFile)
                insertClosedLumiBinds.append( { 'RUN' : 1,
                                                'LUMI' : lumi,
                                                'STREAM' : "A",
                                                'FILECOUNT' : filecount,
                                                'INSERT_TIME' : self.currentTime,
                                                'CLOSE_TIME' : self.currentTime } )
        self.fileset1.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription1)

        self.insertClosedLumiDAO.execute(binds = insertClosedLumiBinds,
                                         transaction = False)

	mySplitArgs['maxInputFiles'] = 5
        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 0,
                         "ERROR: JobFactory should have returned no JobGroup")

        self.insertClosedLumiDAO.execute(binds = { 'RUN' : 1,
                                                   'LUMI' : 3,
                                                   'STREAM' : "A",
                                                   'FILECOUNT' : 0,
                                                   'INSERT_TIME' : self.currentTime,
                                                   'CLOSE_TIME' : self.currentTime },
                                         transaction = False)

        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup")

        self.assertEqual(len(jobGroups[0].jobs), 1,
                         "ERROR: JobFactory didn't create one job")

        self.assertEqual(len(jobGroups[0].jobs[0].getFiles()), 4,
                         "ERROR: first job does not process 4 files")


        return

    def test06(self):
        """
        _test06_

        Test repacking of 3 lumis
        2 small lumis (single job), followed by a big one (multiple jobs)

        files for lumi 1 and 2 are below multi-lumi thresholds
        files for lumi 3 are above single-lumi threshold

        """
        mySplitArgs = self.splitArgs.copy()

        insertClosedLumiBinds = []
        for lumi in [1, 2, 3]:
            filecount = 2
            for i in range(filecount):
                if lumi == 3:
                    nevents = 500
                else:
                    nevents = 100
                newFile = File(makeUUID(), size = 1000, events = nevents)
                newFile.addRun(Run(1, *[lumi]))
                newFile.setLocation("SomePNN", immediateSave = False)
                newFile.create()
                self.fileset1.addFile(newFile)
                insertClosedLumiBinds.append( { 'RUN' : 1,
                                                'LUMI' : lumi,
                                                'STREAM' : "A",
                                                'FILECOUNT' : filecount,
                                                'INSERT_TIME' : self.currentTime,
                                                'CLOSE_TIME' : self.currentTime } )
        self.fileset1.commit()

        jobFactory = self.splitterFactory(package = "WMCore.WMBS",
                                          subscription = self.subscription1)

        self.insertClosedLumiDAO.execute(binds = insertClosedLumiBinds,
                                         transaction = False)

	mySplitArgs['maxInputEvents'] = 900
        jobGroups = jobFactory(**mySplitArgs)

        self.assertEqual(len(jobGroups), 1,
                         "ERROR: JobFactory didn't return one JobGroup")

        self.assertEqual(len(jobGroups[0].jobs), 3,
                         "ERROR: JobFactory didn't create three jobs")

        self.assertEqual(len(jobGroups[0].jobs[0].getFiles()), 4,
                         "ERROR: first job does not process 4 files")

	self.assertEqual(len(jobGroups[0].jobs[1].getFiles()), 1,
                         "ERROR: second job does not process 1 file")

        self.assertEqual(len(jobGroups[0].jobs[2].getFiles()), 1,
                         "ERROR: third job does not process 1 file")

        return

if __name__ == '__main__':
    unittest.main()
