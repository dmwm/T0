#!/usr/bin/env python
"""
_Express_t_

Test for Express job splitter
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
                                             split_algo = "Express",
                                             type = "Express")

        wmbsJobFactory = self.splitterFactory(package = "WMCore.DataStructs",
                                              subscription = self.testSubscription)

        return

    def test01(self):
        """
        _test01_

        Test that the job name prefix feature works
        Test event threshold

        Uses 3 input files
        """
        return

    def test02(self):
        """
        _test02_

        Test multi lumis

        Uses 2 input files
        """
        return

if __name__ == '__main__':
    unittest.main()
