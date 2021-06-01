#!/usr/bin/env python
#pylint: disable-msg=W0613
"""
_Tier0Auditor_

Component wrapper, for real work look at Tier0AuditorPoller

"""

import logging
import threading

# harness class that encapsulates the basic component logic.
from WMCore.Agent.Harness import Harness

from T0Component.Tier0Auditor.Tier0AuditorPoller import Tier0AuditorPoller




class Tier0Auditor(Harness):
    """
    Creates jobs for new subscriptions
    Handler implementation for polling
    
    """

    def __init__(self, config):
        # call the base class
        Harness.__init__(self, config)
        self.pollTime = 1

        print("Tier0Auditor.__init__")

    def preInitialization(self):
        """
        Step that actually adds the worker thread properly

        """
        print("Tier0Auditor.preInitialization")


        # Add event loop to worker manager
        myThread = threading.currentThread()
        
        pollInterval = self.config.Tier0Auditor.pollInterval
        logging.info("Setting poll interval to %s seconds" % pollInterval)
        myThread.workerThreadManager.addWorker(Tier0AuditorPoller(self.config), \
                                               pollInterval)
        return
