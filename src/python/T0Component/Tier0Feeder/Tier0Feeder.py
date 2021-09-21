#!/usr/bin/env python
#pylint: disable-msg=W0613
"""
_Tier0Feeder_

Component wrapper, for real work look at Tier0FeederPoller

"""

import logging
import threading

# harness class that encapsulates the basic component logic.
from WMCore.Agent.Harness import Harness

from T0Component.Tier0Feeder.Tier0FeederPoller import Tier0FeederPoller




class Tier0Feeder(Harness):
    """
    Creates jobs for new subscriptions
    Handler implementation for polling
    
    """

    def __init__(self, config):
        # call the base class
        Harness.__init__(self, config)
        self.pollTime = 1

        print("Tier0Feeder.__init__")

    def preInitialization(self):
        """
        Step that actually adds the worker thread properly

        """
        print("Tier0Feeder.preInitialization")


        # Add event loop to worker manager
        myThread = threading.currentThread()
        
        pollInterval = self.config.Tier0Feeder.pollInterval
        logging.info("Setting poll interval to %s seconds" % pollInterval)
        myThread.workerThreadManager.addWorker(Tier0FeederPoller(self.config), \
                                               pollInterval)
        return
