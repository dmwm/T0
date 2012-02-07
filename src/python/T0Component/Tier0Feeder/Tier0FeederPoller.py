#!/usr/bin/env python
#pylint: disable-msg=W0613, W6501
"""
_Tier0FeederPoller_

The actual work done by the Tier0Feeder component

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

from T0.RunConfig import RunConfigAPI
from T0.RunLumiCloseout import RunLumiCloseoutAPI


class Tier0FeederPoller(BaseWorkerThread):

    def __init__(self, config):
        """
        _init_

        """
        BaseWorkerThread.__init__(self)

        myThread = threading.currentThread()

        self.daoFactory = DAOFactory(package = "T0.WMBS",
                                     logger = logging,
                                     dbinterface = myThread.dbi)

        self.tier0ConfigFile = config.Tier0Feeder.tier0ConfigFile

        hltConfConnectUrl = config.HLTConfDatabase.connectUrl
        dbFactoryHltConf = DBFactory(logging, dburl = hltConfConnectUrl, options = {})
        dbInterfaceHltConf = dbFactoryHltConf.connect()

        daoFactoryHltConf = DAOFactory(package = "T0.WMBS",
                                       logger = logging,
                                       dbinterface = dbInterfaceHltConf)

        self.getHLTConfigDAO = daoFactoryHltConf(classname = "RunConfig.GetHLTConfig")

        storageManagerConnectUrl = config.StorageManagerDatabase.connectUrl
        dbFactoryStorageManager = DBFactory(logging, dburl = storageManagerConnectUrl, options = {})
        self.dbInterfaceStorageManager = dbFactoryStorageManager.connect()

        return

    def algorithm(self, parameters = None):
        """
        _algorithm_

        """
        logging.debug("Running Tier0Feeder algorithm...")
        myThread = threading.currentThread()

        findNewRunsDAO = self.daoFactory(classname = "Tier0Feeder.FindNewRuns")
        findNewRunStreamsDAO = self.daoFactory(classname = "Tier0Feeder.FindNewRunStreams")
        feedStreamersDAO = self.daoFactory(classname = "Tier0Feeder.FeedStreamers")

        tier0Config = None
        try:
            tier0Config = loadConfigurationFile(self.tier0ConfigFile)
        except:
            # usually happens when there are syntax errors in the configuration
            logging.exception("Cannot load Tier0 configuration file, not configuring new runs and run/streams")

        # only configure new runs and run/streams if we have a valid Tier0 configuration
        if tier0Config != None:

            #
            # find new runs, setup global run settings and stream/dataset/trigger mapping
            #
            runHltkeys = findNewRunsDAO.execute(transaction = False)
            for run, hltkey in sorted(runHltkeys.items()):

                hltConfig = None

                # local runs have no hltkey and are configured differently
                if hltkey != None:

                    # retrieve HLT configuration and make sure it's usable
                    try:
                        hltConfig = self.getHLTConfigDAO.execute(hltkey, transaction = False)
                        if hltConfig['process'] == None or len(hltConfig['mapping']) == 0:
                            raise RuntimeError, "HLTConfDB query returned no process or mapping"
                    except:
                        logging.exception("Can't retrieve hltkey %s for run %d" % (hltkey, run))
                        continue

                try:
                    RunConfigAPI.configureRun(tier0Config, run, hltConfig)
                except:
                    logging.exception("Can't configure for run %d" % (run))

            #
            # find unconfigured run/stream with data
            # populate RunConfig, setup workflows/filesets/subscriptions
            # 
            runStreams = findNewRunStreamsDAO.execute(transaction = False)
            for run in sorted(runStreams.keys()):
                for stream in sorted(runStreams[run]):
                    try:
                        RunConfigAPI.configureRunStream(tier0Config, run, stream)
                    except:
                        logging.exception("Can't configure for run %d and stream %s" % (run, stream))

        #
        # close stream/lumis for run/streams that are configured and where the run is active
        #
        RunLumiCloseoutAPI.closeLumiSections(self.dbInterfaceStorageManager)

        #
        # feed new data into exisiting filesets
        #
        try:
            feedStreamersDAO.execute(transaction = False)
        except:
            logging.exception("Can't feed data, bailing out...")
            raise

        return

    def terminate(self, params):
        """
        _terminate_

        Kill the code after one final pass when called by the master thread.

        """
        logging.debug("terminating immediately")
