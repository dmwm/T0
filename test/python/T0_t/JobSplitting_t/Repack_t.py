#!/usr/bin/env python
"""
_Repack_t_

Test for Repack job splitter
"""

import unittest

from WMCore.DataStructs.File import File
from WMCore.DataStructs.Fileset import Fileset
from WMCore.DataStructs.Job import Job
from WMCore.DataStructs.Subscription import Subscription
from WMCore.DataStructs.Workflow import Workflow

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
        self.testInit.setSchema(customModules = ["WMCore.WMBS",
                                                 "T0.WMBS"],
                                useDefault = False)

        self.splitterFactory = SplitterFactory(package = "T0.JobSplitting")

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

        Test to just instantiate the job splitter
        """
        testWorkflow = Workflow()

        self.testFileset = Fileset(name = "TestFileset")
        newFile = File("/some/file/name", size = 1, events = 1)
        self.testFileset.addFile( File("/some/file/name",
                                       size = 1, events = 1) )

        self.testSubscription = Subscription(fileset = self.testFileset,
                                             workflow = testWorkflow,
                                             split_algo = "Repack",
                                             type = "Repack")

        wmbsJobFactory = self.splitterFactory(package = "WMCore.DataStructs",
                                              subscription = self.testSubscription)

        return

    def test01(self):
        """
        _test01_

        Test that the job name prefix feature works
        Test single lumi size threshold

        Uses 1 input file
        """
        return

    def test02(self):
        """
        _test02_

        Test single lumi event threshold

        Uses 1 input file
        """
        return

    def test03(self):
        """
        _test03_

        Test multi lumi size threshold

        Uses 1 input files
        """
        return

    def test04(self):
        """
        _test04_

        Test multi lumi event threshold

        Uses 1 input files
        """
        return

    def test05(self):
        """
        _test05_

        Test streamer count threshold

        Uses 2 input files
        """
        return

    def test06(self):
        """
        _test06_

        Test multi lumi event threshold

        Uses 1 input files
        """
        return

    def test07(self):
        """
        _test07_

        Test closeout (end of run)

        Uses 1 input files
        """
        return

    def test08(self):
        """
        _test08_

        Test how a small lumi followed
        by a very large lumi are treated

        Uses 2 input files
        """
        return

if __name__ == '__main__':
    unittest.main()
