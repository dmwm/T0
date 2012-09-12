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
from WMCore.Services.WMStats.WMStatsWriter import WMStatsWriter

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
        self.specDirectory = config.Tier0Feeder.specDirectory
        self.lfnBase = getattr(config.Tier0Feeder, "lfnBase", "/store")
        self.condUploadDir = config.Tier0Feeder.conditionUploadDir
        self.dqmUploadProxy = config.WMBSService.proxy
        self.localSummaryCouchDB = WMStatsWriter(config.AnalyticsDataCollector.localWMStatsURL)

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

        self.getExpressReadyRunsDAO = None
        if hasattr(config, "PopConLogDatabase"):
            popConLogConnectUrl = getattr(config.PopConLogDatabase, "connectUrl", None)
            if popConLogConnectUrl != None:
                dbFactoryPopConLog = DBFactory(logging, dburl = popConLogConnectUrl, options = {})
                dbInterfacePopConLog = dbFactoryPopConLog.connect()
                daoFactoryPopConLog = DAOFactory(package = "T0.WMBS",
                                                 logger = logging,
                                                 dbinterface = dbInterfacePopConLog)
                self.getExpressReadyRunsDAO = daoFactoryPopConLog(classname = "Tier0Feeder.GetExpressReadyRuns")

        return

    def algorithm(self, parameters = None):
        """
        _algorithm_

        """
        logging.debug("Running Tier0Feeder algorithm...")
        myThread = threading.currentThread()

        findNewRunsDAO = self.daoFactory(classname = "Tier0Feeder.FindNewRuns")
        findNewRunStreamsDAO = self.daoFactory(classname = "Tier0Feeder.FindNewRunStreams")
        findNewExpressRunsDAO = self.daoFactory(classname = "Tier0Feeder.FindNewExpressRuns")
        releaseExpressDAO = self.daoFactory(classname = "Tier0Feeder.ReleaseExpress")
        feedStreamersDAO = self.daoFactory(classname = "Tier0Feeder.FeedStreamers")
        markRepackInjectedDAO = self.daoFactory(classname = "Tier0Feeder.MarkRepackInjected")

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
                    RunConfigAPI.configureRun(tier0Config, run, self.lfnBase, hltConfig)
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
                        RunConfigAPI.configureRunStream(tier0Config,
                                                        run, stream,
                                                        self.specDirectory,
                                                        self.condUploadDir,
                                                        self.dqmUploadProxy)
                    except:
                        logging.exception("Can't configure for run %d and stream %s" % (run, stream))

        #
        # end runs which are active and have ended according to the EoR StorageManager records
        #
        RunLumiCloseoutAPI.endRuns(self.dbInterfaceStorageManager)

        #
        # release runs for Express
        #
        runs = findNewExpressRunsDAO.execute(transaction = False)

        if len(runs) > 0:

            binds = []
            for run in runs:
                binds.append( { 'RUN' : run } )

            if self.getExpressReadyRunsDAO != None:
                runs = self.getExpressReadyRunsDAO.execute(binds = binds, transaction = False)

            if len(runs) > 0:

                binds = []
                for run in runs:
                    binds.append( { 'RUN' : run } )

                releaseExpressDAO.execute(binds = binds, transaction = False)

        #
        # release runs for PromptReco
        #
        RunConfigAPI.releasePromptReco(tier0Config,
                                       self.specDirectory,
				       self.dqmUploadProxy)

        #
        # check if all datasets for a stream had their PromptReco released
        # then mark the repack workflow as injected (if we don't wait, the
        # task archiver will cleanup too early)
        #
        markRepackInjectedDAO.execute(transaction = False)

        #
        # close stream/lumis for run/streams that are active (fileset exists and open)
        #
        RunLumiCloseoutAPI.closeLumiSections(self.dbInterfaceStorageManager)

        #
        # feed new data into exisiting filesets
        #
        try:
            myThread.transaction.begin()
            feedStreamersDAO.execute(conn = myThread.transaction.conn, transaction = True)
        except:
            logging.exception("Can't feed data, bailing out...")
            raise
        else:
            myThread.transaction.commit()

        #
        # run ended and run/stream fileset open
        #    => check for complete lumi_closed record, all lumis finally closed and all data feed
        #          => if all conditions satisfied, close the run/stream fileset
        #
        RunLumiCloseoutAPI.closeRunStreamFilesets()

        #
        # check and delete active split lumis
        #
        RunLumiCloseoutAPI.checkActiveSplitLumis()
        
        # gets all workflows not inserted to couchDB and does it.
        self.feedCouchMonitoring()

        return

    def feedCouchMonitoring(self):

        getPendingWorkflowMonitoringDAO = self.daoFactory(classname = "Tier0Feeder.GetPendingWorkflowMonitoring")
        markTrackedWorkflowMonitoringDAO = self.daoFactory(classname = "Tier0Feeder.MarkTrackedWorkflowMonitoring")
        workflows = getPendingWorkflowMonitoringDAO.execute()
        if len(workflows) == 0:
            logging.debug("No workflows to publish to couch monitoring, doing nothing")
        if workflows:
            logging.debug(" Going to publish %d workflows" % len(workflows))
            for (workflowId, run, workflowName) in workflows:
                logging.info(" Publishing workflow %s to monitoring" % workflowName)
                doc = {}
                doc["_id"] =  str(workflowId)
                doc["workflow"] =   workflowName
                doc["type"]     =   "tier0_request"
                doc["run"]      =   run
                response = self.localSummaryCouchDB.insertGenericRequest(doc)
                if response == "OK" or "EXISTS":
                    logging.info(" Successfully uploaded request %s" % workflowName)
                    # Here we have to trust the insert, if it doesn't happen will be easy to spot on the logs
                    markTrackedWorkflowMonitoringDAO.execute(workflowId)

    def terminate(self, params):
        """
        _terminate_

        Kill the code after one final pass when called by the master thread.

        """
        logging.debug("terminating immediately")
