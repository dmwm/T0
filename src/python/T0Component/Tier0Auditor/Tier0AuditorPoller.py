#!/usr/bin/env python
#pylint: disable-msg=W0613
"""
_Tier0AuditorPoller_

The actual work done by the Tier0Auditor component

Checks for new data
Populates RunConfig for new runs
Setup subscriptions for new runs/streams
Assigns new data to the correct subscriptions

"""
import logging
import threading

from WMCore.WorkerThreads.BaseWorkerThread import BaseWorkerThread
from WMCore.DAOFactory import DAOFactory
from WMCore.Database.DBFactory import DBFactory
from WMCore.WMException import WMException
from WMCore.Configuration import loadConfigurationFile

from T0.RunLumiCloseout import RunLumiCloseoutAPI


class Tier0AuditorPoller(BaseWorkerThread):

    def __init__(self, config):
        """
        _init_

        """
        BaseWorkerThread.__init__(self)

        myThread = threading.currentThread()

        self.daoFactory = DAOFactory(package = "T0.WMBS",
                                     logger = logging,
                                     dbinterface = myThread.dbi)

        return

    def algorithm(self, parameters = None):
        """
        _algorithm_

        """
        logging.debug("Running Tier0Auditor algorithm...")
        myThread = threading.currentThread()

        return

    def terminate(self, params):
        """
        _terminate_

        Kill the code after one final pass when called by the master thread.

        """
        logging.debug("terminating immediately")
