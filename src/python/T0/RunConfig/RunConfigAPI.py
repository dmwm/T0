"""
_RunConfigAPI_

API for anyting RunConfig related

"""
import logging
import threading
import time

from WMCore.DAOFactory import DAOFactory

from WMCore.WorkQueue.WMBSHelper import WMBSHelper
from WMCore.WMBS.Fileset import Fileset

from T0.RunConfig.Tier0Config import retrieveDatasetConfig
from T0.RunConfig.Tier0Config import addRepackConfig
from T0.RunConfig.Tier0Config import deleteStreamConfig

from T0.WMSpec.StdSpecs.Repack import getTestArguments as getRepackArguments
from T0.WMSpec.StdSpecs.Repack import repackWorkload
from T0.WMSpec.StdSpecs.Express import getTestArguments as getExpressArguments
from T0.WMSpec.StdSpecs.Express import expressWorkload
from WMCore.WMSpec.StdSpecs.PromptReco import getTestArguments as getPromptRecoArguments
from WMCore.WMSpec.StdSpecs.PromptReco import promptrecoWorkload

def configureRun(tier0Config, run, hltConfig, referenceHltConfig = None):
    """
    _configureRun_

    Called by Tier0Feeder for new runs.

    Retrieve HLT config and configure global run
    settings and stream/dataset/trigger mapping

    """
    logging.debug("configureRun() : %d" % run)
    myThread = threading.currentThread()

    daoFactory = DAOFactory(package = "T0.WMBS",
                            logger = logging,
                            dbinterface = myThread.dbi)

    # dao to update global run settings
    updateRunDAO = daoFactory(classname = "RunConfig.UpdateRun")

    # workaround to make unit test work without HLTConfDatabase
    if hltConfig == None and referenceHltConfig != None:
        hltConfig = referenceHltConfig

    #
    # treat centralDAQ or miniDAQ runs (have an HLT key) different from local runs
    #
    if hltConfig != None:

        # write stream/dataset/trigger mapping
        insertStreamDAO = daoFactory(classname = "RunConfig.InsertStream")
        insertDatasetDAO = daoFactory(classname = "RunConfig.InsertPrimaryDataset")
        insertStreamDatasetDAO = daoFactory(classname = "RunConfig.InsertStreamDataset")
        insertTriggerDAO = daoFactory(classname = "RunConfig.InsertTrigger")
        insertDatasetTriggerDAO = daoFactory(classname = "RunConfig.InsertDatasetTrigger")

        bindsUpdateRun = { 'RUN' : run,
                           'PROCESS' : hltConfig['process'],
                           'ACQERA' : tier0Config.Global.AcquisitionEra,
                           'LFNPREFIX' : tier0Config.Global.LFNPrefix,
                           'BULKDATATYPE' : tier0Config.Global.BulkDataType,
                           'BULKDATALOC' : tier0Config.Global.BulkDataLocation,
                           'DQMUPLOADURL' : tier0Config.Global.DQMUploadUrl,
                           'AHTIMEOUT' : tier0Config.Global.AlcaHarvestTimeout,
                           'AHDIR' : tier0Config.Global.AlcaHarvestDir,
                           'CONDTIMEOUT' : tier0Config.Global.ConditionUploadTimeout,
                           'DBHOST' : tier0Config.Global.DropboxHost,
                           'VALIDMODE' : tier0Config.Global.ValidationMode }

        bindsStream = []
        bindsDataset = []
        bindsStreamDataset = []
        bindsTrigger = []
        bindsDatasetTrigger = []
        for stream, datasetDict in hltConfig['mapping'].items():
            bindsStream.append( { 'STREAM' : stream } )
            for dataset, paths in datasetDict.items():
                bindsDataset.append( { 'PRIMDS' : dataset } )
                bindsStreamDataset.append( { 'RUN' : run,
                                             'PRIMDS' : dataset,
                                             'STREAM' : stream } )
                for path in paths:
                    bindsTrigger.append( { 'TRIG' : path } )
                    bindsDatasetTrigger.append( { 'RUN' : run,
                                                  'TRIG' : path,
                                                  'PRIMDS' : dataset } )

        try:
            myThread.transaction.begin()
            updateRunDAO.execute(bindsUpdateRun, conn = myThread.transaction.conn, transaction = True)
            insertStreamDAO.execute(bindsStream, conn = myThread.transaction.conn, transaction = True)
            insertDatasetDAO.execute(bindsDataset, conn = myThread.transaction.conn, transaction = True)
            insertStreamDatasetDAO.execute(bindsStreamDataset, conn = myThread.transaction.conn, transaction = True)
            insertTriggerDAO.execute(bindsTrigger, conn = myThread.transaction.conn, transaction = True)
            insertDatasetTriggerDAO.execute(bindsDatasetTrigger, conn = myThread.transaction.conn, transaction = True)
        except:
            myThread.transaction.rollback()
            raise
        else:
            myThread.transaction.commit()

    else:

        bindsUpdateRun = { 'RUN' : run,
                           'PROCESS' : "FakeProcessName",
                           'ACQERA' : "FakeAcquisitionEra",
                           'LFNPREFIX' : "/fakelfnprefix",
                           'BULKDATATYPE' : "FakeBulkDataType",
                           'AHTIMEOUT' : None,
                           'AHDIR' : None,
                           'CONDTIMEOUT' : None,
                           'DBHOST' : None,
                           'VALIDMODE' : None }

        try:
            myThread.transaction.begin()
            updateRunDAO.execute(bindsUpdateRun, conn = myThread.transaction.conn, transaction = True)
        except:
            myThread.transaction.rollback()
            raise
        else:
            myThread.transaction.commit()

    return

def configureRunStream(tier0Config, run, stream, specDirectory, dqmUploadProxy):
    """
    _configureRunStream_

    Called by Tier0Feeder for new run/streams.

    Retrieve global run settings and build the part
    of the configuration relevant to run/stream
    and write it to the database.

    Create workflows, filesets and subscriptions for
    the processing of runs/streams.

    """
    logging.debug("configureRunStream() : %d , %s" % (run, stream))
    myThread = threading.currentThread()

    daoFactory = DAOFactory(package = "T0.WMBS",
                            logger = logging,
                            dbinterface = myThread.dbi)

    # retrieve some basic run information
    getRunInfoDAO = daoFactory(classname = "RunConfig.GetRunInfo")
    runInfo = getRunInfoDAO.execute(run, transaction = False)[0]

    #
    # treat centralDAQ or miniDAQ runs (have an HLT key) different from local runs
    #
    if runInfo['hltkey'] != None:

        # streams not explicitely configured are repacked
        if stream not in tier0Config.Streams.dictionary_().keys():
            addRepackConfig(tier0Config, stream)

        streamConfig = tier0Config.Streams.dictionary_()[stream]

        # write stream/dataset mapping (for special express and error datasets)
        insertDatasetDAO = daoFactory(classname = "RunConfig.InsertPrimaryDataset")
        insertStreamDatasetDAO = daoFactory(classname = "RunConfig.InsertStreamDataset")

        # write stream configuration
        insertStreamStyleDAO = daoFactory(classname = "RunConfig.InsertStreamStyle")
        insertRepackConfigDAO = daoFactory(classname = "RunConfig.InsertRepackConfig")
        insertPromptCalibrationDAO = daoFactory(classname = "RunConfig.InsertPromptCalibration")
        insertExpressConfigDAO = daoFactory(classname = "RunConfig.InsertExpressConfig")
        insertSpecialDatasetDAO = daoFactory(classname = "RunConfig.InsertSpecialDataset")
        insertDatasetScenarioDAO = daoFactory(classname = "RunConfig.InsertDatasetScenario")
        insertCMSSWVersionDAO = daoFactory(classname = "RunConfig.InsertCMSSWVersion")
        updateStreamOverrideDAO = daoFactory(classname = "RunConfig.UpdateStreamOverride")
        insertStreamFilesetDAO = daoFactory(classname = "RunConfig.InsertStreamFileset")
        insertRecoReleaseConfigDAO = daoFactory(classname = "RunConfig.InsertRecoReleaseConfig")
        insertWorkflowMonitoringDAO = daoFactory(classname = "RunConfig.InsertWorkflowMonitoring")
        insertStorageNodeDAO = daoFactory(classname = "RunConfig.InsertStorageNode")
        insertPhEDExConfigDAO = daoFactory(classname = "RunConfig.InsertPhEDExConfig")

        bindsDataset = []
        bindsStreamDataset = []
        bindsStreamStyle = {'RUN' : run,
                            'STREAM' : stream,
                            'STYLE': streamConfig.ProcessingStyle }
        bindsRepackConfig = {}
        bindsPromptCalibration = {}
        bindsExpressConfig = {}
        bindsSpecialDataset = {}
        bindsDatasetScenario = []
        bindsCMSSWVersion = []
        bindsStreamOverride = {}
        bindsStorageNode = []
        bindsPhEDExConfig = []

        # mark workflows as injected
        wmbsDaoFactory = DAOFactory(package = "WMCore.WMBS",
                                    logger = logging,
                                    dbinterface = myThread.dbi)
        markWorkflowsInjectedDAO = wmbsDaoFactory(classname = "Workflow.MarkInjectedWorkflows")

        #
        # for spec creation, details for all outputs
        #
        outputModuleDetails = []

        #
        # for PromptReco delay settings
        #
        promptRecoDelay = {}
        promptRecoDelayOffset = {}

        #
        # for PhEDEx subscription settings
        #
        subscriptions = { 'Express' : [],
                          'Bulk' : [] }

        # some hardcoded PhEDEx defaults
        expressPhEDExInjectNode = "T2_CH_CERN"
        expressPhEDExSubscribeNode = "T2_CH_CERN"

        #
        # first take care of all stream settings
        #
        getStreamOnlineVersionDAO = daoFactory(classname = "RunConfig.GetStreamOnlineVersion")
        onlineVersion = getStreamOnlineVersionDAO.execute(run, stream, transaction = False)

        if streamConfig.ProcessingStyle == "Bulk":

            bindsRepackConfig = { 'RUN' : run,
                                  'STREAM' : stream,
                                  'PROC_VER': streamConfig.Repack.ProcessingVersion,
                                  'MAX_SIZE_SINGLE_LUMI' : streamConfig.Repack.MaxSizeSingleLumi,
                                  'MAX_SIZE_MULTI_LUMI' : streamConfig.Repack.MaxSizeMultiLumi,
                                  'MIN_SIZE' : streamConfig.Repack.MinInputSize,
                                  'MAX_SIZE' : streamConfig.Repack.MaxInputSize,
                                  'MAX_EDM_SIZE' : streamConfig.Repack.MaxEdmSize,
                                  'MAX_OVER_SIZE' : streamConfig.Repack.MaxOverSize,
                                  'MAX_EVENTS' : streamConfig.Repack.MaxInputEvents,
                                  'MAX_FILES' : streamConfig.Repack.MaxInputFiles }

        elif streamConfig.ProcessingStyle == "Express":

            specialDataset = "Stream%s" % stream
            bindsDataset.append( { 'PRIMDS' : specialDataset } )
            bindsStreamDataset.append( { 'RUN' : run,
                                         'PRIMDS' : specialDataset,
                                         'STREAM' : stream } )
            bindsSpecialDataset = { 'STREAM' : stream,
                                    'PRIMDS' : specialDataset }
            bindsDatasetScenario.append( { 'RUN' : run,
                                           'PRIMDS' : specialDataset,
                                           'SCENARIO' : streamConfig.Express.Scenario } )

            if "DQM" in streamConfig.Express.DataTiers:
                outputModuleDetails.append( { 'dataTier' : "DQM",
                                              'eventContent' : "DQM",
                                              'primaryDataset' : specialDataset } )

            bindsStorageNode.append( { 'NODE' : expressPhEDExSubscribeNode } )

            bindsPhEDExConfig.append( { 'RUN' : run,
                                        'PRIMDS' : specialDataset,
                                        'NODE' : expressPhEDExSubscribeNode,
                                        'CUSTODIAL' : 1,
                                        'REQ_ONLY' : "n",
                                        'PRIO' : "high" } )

            subscriptions['Express'].append( { 'custodialSites' : [],
                                               'nonCustodialSites' : [expressPhEDExSubscribeNode],
                                               'autoApproveSites' : [expressPhEDExSubscribeNode],
                                               'priority' : "high",
                                               'primaryDataset' : specialDataset } )

            alcaSkim = None
            if "ALCARECO" in streamConfig.Express.DataTiers:
                if len(streamConfig.Express.AlcaSkims) > 0:
                    outputModuleDetails.append( { 'dataTier' : "ALCARECO",
                                                  'eventContent' : "ALCARECO",
                                                  'primaryDataset' : specialDataset } )
                    alcaSkim = ",".join(streamConfig.Express.AlcaSkims)

                    if "PromptCalibProd" in streamConfig.Express.AlcaSkims:
                        bindsPromptCalibration = { 'RUN' : run,
                                                   'STREAM' : stream }

            dqmSeq = None
            if len(streamConfig.Express.DqmSequences) > 0:
                dqmSeq = ",".join(streamConfig.Express.DqmSequences)

            bindsExpressConfig = { 'RUN' : run,
                                   'STREAM' : stream,
                                   'PROC_VER' : streamConfig.Express.ProcessingVersion,
                                   'WRITE_TIERS' : ",".join(streamConfig.Express.DataTiers),
                                   'GLOBAL_TAG' : streamConfig.Express.GlobalTag,
                                   'MAX_EVENTS' : streamConfig.Express.MaxInputEvents,
                                   'MAX_SIZE' : streamConfig.Express.MaxInputSize,
                                   'MAX_FILES' : streamConfig.Express.MaxInputFiles,
                                   'MAX_LATENCY' : streamConfig.Express.MaxLatency,
                                   'BLOCK_DELAY' : streamConfig.Express.BlockCloseDelay,
                                   'ALCA_SKIM' : alcaSkim,
                                   'DQM_SEQ' : dqmSeq }

        overrideVersion = streamConfig.VersionOverride.get(onlineVersion, None)
        if overrideVersion != None:
            bindsCMSSWVersion.append( { 'VERSION' : overrideVersion } )
            bindsStreamOverride =  { "RUN" : run,
                                     "STREAM" : stream,
                                     "OVERRIDE" : overrideVersion }

        #
        # then configure datasets
        #
        getStreamDatasetTriggersDAO = daoFactory(classname = "RunConfig.GetStreamDatasetTriggers")
        datasetTriggers = getStreamDatasetTriggersDAO.execute(run, stream, transaction = False)

        for dataset, paths in datasetTriggers.items():

            if dataset == "Unassigned path":
                if stream == "Express" and run in [ 210114, 210116, 210120, 210121, 210178 ]:
                    continue

            datasetConfig = retrieveDatasetConfig(tier0Config, dataset)

            selectEvents = []
            for path in sorted(paths):
                selectEvents.append("%s:%s" % (path, runInfo['process']))

            if streamConfig.ProcessingStyle == "Bulk":

                promptRecoDelay[datasetConfig.Name] = datasetConfig.RecoDelay
                promptRecoDelayOffset[datasetConfig.Name] = datasetConfig.RecoDelayOffset

                outputModuleDetails.append( { 'dataTier' : "RAW",
                                              'eventContent' : "ALL",
                                              'selectEvents' : selectEvents,
                                              'primaryDataset' : dataset } )

                custodialSites = []
                nonCustodialSites = []
                autoApproveSites = []

                if datasetConfig.CustodialNode != None:

                    custodialSites.append(datasetConfig.CustodialNode)

                    requestOnly = "y"
                    if datasetConfig.CustodialAutoApprove:
                        requestOnly = "n"
                        autoApproveSites.append(datasetConfig.CustodialNode)

                    bindsStorageNode.append( { 'NODE' : datasetConfig.CustodialNode } )

                    bindsPhEDExConfig.append( { 'RUN' : run,
                                                'PRIMDS' : dataset,
                                                'NODE' : datasetConfig.CustodialNode,
                                                'CUSTODIAL' : 1,
                                                'REQ_ONLY' : requestOnly,
                                                'PRIO' : datasetConfig.CustodialPriority } )

                if datasetConfig.ArchivalNode != None:

                    custodialSites.append(datasetConfig.ArchivalNode)
                    autoApproveSites.append(datasetConfig.ArchivalNode)

                    bindsStorageNode.append( { 'NODE' : datasetConfig.ArchivalNode } )

                    bindsPhEDExConfig.append( { 'RUN' : run,
                                                'PRIMDS' : dataset,
                                                'NODE' : datasetConfig.ArchivalNode,
                                                'CUSTODIAL' : 1,
                                                'REQ_ONLY' : "n",
                                                'PRIO' : datasetConfig.CustodialPriority } )

                if len(custodialSites) + len(nonCustodialSites) > 0:
                    subscriptions['Bulk'].append( { 'custodialSites' : custodialSites,
                                                    'nonCustodialSites' : nonCustodialSites,
                                                    'autoApproveSites' : autoApproveSites,
                                                    'priority' : datasetConfig.CustodialPriority,
                                                    'primaryDataset' : dataset } )

            elif streamConfig.ProcessingStyle == "Express":

                for dataTier in streamConfig.Express.DataTiers:
                    if dataTier not in [ "ALCARECO", "DQM" ]:

                        outputModuleDetails.append( { 'dataTier' : dataTier,
                                                      'eventContent' : dataTier,
                                                      'selectEvents' : selectEvents,
                                                      'primaryDataset' : dataset } )

                bindsPhEDExConfig.append( { 'RUN' : run,
                                            'PRIMDS' : dataset,
                                            'NODE' : expressPhEDExSubscribeNode,
                                            'CUSTODIAL' : 1,
                                            'REQ_ONLY' : "n",
                                            'PRIO' : "high" } )

                subscriptions['Express'].append( { 'custodialSites' : [],
                                                   'nonCustodialSites' : [expressPhEDExSubscribeNode],
                                                   'autoApproveSites' : [expressPhEDExSubscribeNode],
                                                   'priority' : "high",
                                                   'primaryDataset' : dataset } )

        #
        # finally create WMSpec
        #
        outputs = {}
        if streamConfig.ProcessingStyle == "Bulk":
            taskName = "Repack"
            workflowName = "Repack_Run%d_Stream%s" % (run, stream)
            specArguments = getRepackArguments()
            specArguments['ProcessingVersion'] = streamConfig.Repack.ProcessingVersion
            specArguments['MaxSizeSingleLumi'] = streamConfig.Repack.MaxSizeSingleLumi
            specArguments['MaxSizeMultiLumi'] = streamConfig.Repack.MaxSizeMultiLumi
            specArguments['MinInputSize'] = streamConfig.Repack.MinInputSize
            specArguments['MaxInputSize'] = streamConfig.Repack.MaxInputSize
            specArguments['MaxEdmSize'] = streamConfig.Repack.MaxEdmSize
            specArguments['MaxOverSize'] = streamConfig.Repack.MaxOverSize
            specArguments['MaxInputEvents'] = streamConfig.Repack.MaxInputEvents
            specArguments['MaxInputFiles'] = streamConfig.Repack.MaxInputFiles
            specArguments['UnmergedLFNBase'] = "%s/t0temp/%s" % (runInfo['lfn_prefix'],
                                                                 runInfo['bulk_data_type'])
            specArguments['MergedLFNBase'] = "%s/%s" % (runInfo['lfn_prefix'],
                                                        runInfo['bulk_data_type'])
        elif streamConfig.ProcessingStyle == "Express":
            taskName = "Express"
            workflowName = "Express_Run%d_Stream%s" % (run, stream)
            specArguments = getExpressArguments()
            specArguments['ProcessingString'] = "Express"
            specArguments['ProcessingVersion'] = streamConfig.Express.ProcessingVersion
            specArguments['ProcScenario'] = streamConfig.Express.Scenario
            specArguments['GlobalTag'] = streamConfig.Express.GlobalTag
            specArguments['GlobalTagTransaction'] = "Express_%d" % run
            specArguments['MaxInputEvents'] = streamConfig.Express.MaxInputEvents
            specArguments['MaxInputSize'] = streamConfig.Express.MaxInputSize
            specArguments['MaxInputFiles'] = streamConfig.Express.MaxInputFiles
            specArguments['MaxLatency'] = streamConfig.Express.MaxLatency
            specArguments['BlockCloseDelay'] = streamConfig.Express.BlockCloseDelay
            specArguments['AlcaSkims'] = streamConfig.Express.AlcaSkims
            specArguments['DqmSequences'] = streamConfig.Express.DqmSequences
            specArguments['UnmergedLFNBase'] = "%s/t0temp/express" % runInfo['lfn_prefix']
            specArguments['MergedLFNBase'] = "%s/express" % runInfo['lfn_prefix']
            specArguments['AlcaHarvestTimeout'] = runInfo['ah_timeout']
            specArguments['AlcaHarvestDir'] = runInfo['ah_dir']
            specArguments['DQMUploadProxy'] = dqmUploadProxy
            specArguments['DQMUploadUrl'] = runInfo['dqmuploadurl']
            specArguments['StreamName'] = stream

        if streamConfig.ProcessingStyle in [ 'Bulk', 'Express' ]:
            specArguments['RunNumber'] = run
            specArguments['AcquisitionEra'] = tier0Config.Global.AcquisitionEra
            specArguments['CMSSWVersion'] = streamConfig.VersionOverride.get(onlineVersion, onlineVersion)
            specArguments['Outputs'] = outputModuleDetails
            specArguments['OverrideCatalog'] = "trivialcatalog_file:/afs/cern.ch/cms/SITECONF/T0_CH_CERN/Tier0/override_catalog.xml?protocol=override"
            specArguments['ValidStatus'] = "VALID"

        if streamConfig.ProcessingStyle == "Bulk":
            wmSpec = repackWorkload(workflowName, specArguments)
            wmSpec.setPhEDExInjectionOverride(runInfo['bulk_data_loc'])
            for subscription in subscriptions['Bulk']:
                wmSpec.setSubscriptionInformation(**subscription)
        elif streamConfig.ProcessingStyle == "Express":
            wmSpec = expressWorkload(workflowName, specArguments)
            wmSpec.setPhEDExInjectionOverride(expressPhEDExInjectNode)
            for subscription in subscriptions['Express']:
                wmSpec.setSubscriptionInformation(**subscription)

        if streamConfig.ProcessingStyle in [ 'Bulk', 'Express' ]:
            wmSpec.setOwnerDetails("Dirk.Hufnagel@cern.ch", "T0",
                                   { 'vogroup': 'DEFAULT', 'vorole': 'DEFAULT',
                                     'dn' : "Dirk.Hufnagel@cern.ch" } )

            wmSpec.setupPerformanceMonitoring(maxRSS = 10485760, maxVSize = 10485760,
                                              softTimeout = 604800, gracePeriod = 3600)

            wmbsHelper = WMBSHelper(wmSpec, taskName, cachepath = specDirectory)

        filesetName = "Run%d_Stream%s" % (run, stream)
        fileset = Fileset(filesetName)

        #
        # create workflow (currently either repack or express)
        #
        try:
            myThread.transaction.begin()
            if len(bindsDataset) > 0:
                insertDatasetDAO.execute(bindsDataset, conn = myThread.transaction.conn, transaction = True)
            if len(bindsStreamDataset) > 0:
                insertStreamDatasetDAO.execute(bindsStreamDataset, conn = myThread.transaction.conn, transaction = True)
            if len(bindsRepackConfig) > 0:
                insertRepackConfigDAO.execute(bindsRepackConfig, conn = myThread.transaction.conn, transaction = True)
            if len(bindsPromptCalibration) > 0:
                insertPromptCalibrationDAO.execute(bindsPromptCalibration, conn = myThread.transaction.conn, transaction = True)
            if len(bindsExpressConfig) > 0:
                insertExpressConfigDAO.execute(bindsExpressConfig, conn = myThread.transaction.conn, transaction = True)
            if len(bindsSpecialDataset) > 0:
                insertSpecialDatasetDAO.execute(bindsSpecialDataset, conn = myThread.transaction.conn, transaction = True)
            if len(bindsDatasetScenario) > 0:
                insertDatasetScenarioDAO.execute(bindsDatasetScenario, conn = myThread.transaction.conn, transaction = True)
            if len(bindsCMSSWVersion) > 0:
                insertCMSSWVersionDAO.execute(bindsCMSSWVersion, conn = myThread.transaction.conn, transaction = True)
            if len(bindsStreamOverride) > 0:
                updateStreamOverrideDAO.execute(bindsStreamOverride, conn = myThread.transaction.conn, transaction = True)
            if len(bindsStorageNode) > 0:
                insertStorageNodeDAO.execute(bindsStorageNode, conn = myThread.transaction.conn, transaction = True)
            if len(bindsPhEDExConfig) > 0:
                insertPhEDExConfigDAO.execute(bindsPhEDExConfig, conn = myThread.transaction.conn, transaction = True)
            insertStreamStyleDAO.execute(bindsStreamStyle, conn = myThread.transaction.conn, transaction = True)
            if streamConfig.ProcessingStyle in [ 'Bulk', 'Express' ]:
                insertStreamFilesetDAO.execute(run, stream, filesetName, conn = myThread.transaction.conn, transaction = True)
                fileset.load()
                wmbsHelper.createSubscription(wmSpec.getTask(taskName), fileset, alternativeFilesetClose = True)
                insertWorkflowMonitoringDAO.execute([fileset.id],  conn = myThread.transaction.conn, transaction = True)
            if streamConfig.ProcessingStyle == "Bulk":
                bindsRecoReleaseConfig = []
                for fileset, primds in wmbsHelper.getMergeOutputMapping().items():
                    bindsRecoReleaseConfig.append( { 'RUN' : run,
                                                     'PRIMDS' : primds,
                                                     'FILESET' : fileset,
                                                     'RECODELAY' : promptRecoDelay[primds],
                                                     'RECODELAYOFFSET' : promptRecoDelayOffset[primds] } )
                insertRecoReleaseConfigDAO.execute(bindsRecoReleaseConfig, conn = myThread.transaction.conn, transaction = True)
            elif streamConfig.ProcessingStyle == "Express":
                markWorkflowsInjectedDAO.execute([workflowName], injected = True, conn = myThread.transaction.conn, transaction = True)
        except:
            myThread.transaction.rollback()
            raise
        else:
            myThread.transaction.commit()

    else:

        # should we do anything for local runs ?
        pass
    return

def releasePromptReco(tier0Config, specDirectory, dqmUploadProxy = None):
    """
    _releasePromptReco_

    Called by Tier0Feeder

    Finds all run/primds that need to be released for PromptReco
    ( run.end_time + reco_release_config.delay > now
      AND run.end_time > 0 )

    Create workflows and subscriptions for the processing
    of runs/datasets.

    """
    logging.debug("releasePromptReco()")
    myThread = threading.currentThread()

    daoFactory = DAOFactory(package = "T0.WMBS",
                            logger = logging,
                            dbinterface = myThread.dbi)

    insertDatasetScenarioDAO = daoFactory(classname = "RunConfig.InsertDatasetScenario")
    insertCMSSWVersionDAO = daoFactory(classname = "RunConfig.InsertCMSSWVersion")
    insertRecoConfigDAO = daoFactory(classname = "RunConfig.InsertRecoConfig")
    insertStorageNodeDAO = daoFactory(classname = "RunConfig.InsertStorageNode")
    insertPhEDExConfigDAO = daoFactory(classname = "RunConfig.InsertPhEDExConfig")
    insertPromptSkimConfigDAO = daoFactory(classname = "RunConfig.InsertPromptSkimConfig")
    releasePromptRecoDAO = daoFactory(classname = "RunConfig.ReleasePromptReco")
    insertWorkflowMonitoringDAO = daoFactory(classname = "RunConfig.InsertWorkflowMonitoring")

    bindsDatasetScenario = []
    bindsCMSSWVersion = []
    bindsRecoConfig = []
    bindsStorageNode = []
    bindsPromptSkimConfig = []
    bindsReleasePromptReco = []

    # mark workflows as injected
    wmbsDaoFactory = DAOFactory(package = "WMCore.WMBS",
                                logger = logging,
                                dbinterface = myThread.dbi)
    markWorkflowsInjectedDAO   = wmbsDaoFactory(classname = "Workflow.MarkInjectedWorkflows")

    #
    # for creating PromptReco specs
    #
    recoSpecs = {}

    #
    # for PhEDEx subscription settings
    #
    subscriptions = []

    findRecoReleaseDAO = daoFactory(classname = "RunConfig.FindRecoRelease")
    recoRelease = findRecoReleaseDAO.execute(transaction = False)

    for run in sorted(recoRelease.keys()):

        # retrieve some basic run information
        getRunInfoDAO = daoFactory(classname = "RunConfig.GetRunInfo")
        runInfo = getRunInfoDAO.execute(run, transaction = False)[0]

        # retrieve phedex configs for run
        getPhEDExConfigDAO = daoFactory(classname = "RunConfig.GetPhEDExConfig")
        phedexConfigs = getPhEDExConfigDAO.execute(run, transaction = False)

        for (dataset, fileset, repackProcVer) in recoRelease[run]:

            bindsReleasePromptReco.append( { 'RUN' : run,
                                             'PRIMDS' : dataset,
                                             'NOW' : int(time.time()) } )

            datasetConfig = retrieveDatasetConfig(tier0Config, dataset)

            bindsDatasetScenario.append( { 'RUN' : run,
                                           'PRIMDS' : dataset,
                                           'SCENARIO' : datasetConfig.Scenario } )

            bindsCMSSWVersion.append( { 'VERSION' : datasetConfig.Reco.CMSSWVersion } )

            alcaSkim = None
            if len(datasetConfig.Reco.AlcaSkims) > 0:
                alcaSkim = ",".join(datasetConfig.Reco.AlcaSkims)

            dqmSeq = None
            if len(datasetConfig.Reco.DqmSequences) > 0:
                dqmSeq = ",".join(datasetConfig.Reco.DqmSequences)

            bindsRecoConfig.append( { 'RUN' : run,
                                      'PRIMDS' : dataset,
                                      'DO_RECO' : int(datasetConfig.Reco.DoReco),
                                      'CMSSW' : datasetConfig.Reco.CMSSWVersion,
                                      'RECO_SPLIT' : datasetConfig.Reco.EventSplit,
                                      'WRITE_RECO' : int(datasetConfig.Reco.WriteRECO),
                                      'WRITE_DQM' : int(datasetConfig.Reco.WriteDQM),
                                      'WRITE_AOD' : int(datasetConfig.Reco.WriteAOD),
                                      'PROC_VER' : datasetConfig.Reco.ProcessingVersion,
                                      'ALCA_SKIM' : alcaSkim,
                                      'DQM_SEQ' : dqmSeq,
                                      'GLOBAL_TAG' : datasetConfig.Reco.GlobalTag } )

            phedexConfig = phedexConfigs[dataset]

            custodialSites = []
            nonCustodialSites = []
            autoApproveSites = []

            for node, config in phedexConfig.items():

                if config['custodial'] == 1:
                    custodialSites.append(node)
                else:
                    nonCustodialSites.append(node)

                if config['request_only'] == "n":
                    autoApproveSites.append(node)

            if len(custodialSites) + len(nonCustodialSites) > 0:
                subscriptions.append( { 'custodialSites' : custodialSites,
                                        'nonCustodialSites' : nonCustodialSites,
                                        'autoApproveSites' : autoApproveSites,
                                        'priority' : config['priority'],
                                        'primaryDataset' : dataset } )

            for tier1Skim in datasetConfig.Tier1Skims:

                bindsCMSSWVersion.append( { 'VERSION' : tier1Skim.CMSSWVersion } )

                if tier1Skim.Node == None:
                    tier1Skim.Node = datasetConfig.CustodialNode
                else:
                    bindsStorageNode.append( { 'NODE' : tier1Skim.Node } )

                if tier1Skim.Node == None:
                    raise RuntimeError, "Configured a skim without providing a skim node or a custodial site\n"

                bindsPromptSkimConfig.append( { 'RUN' : run,
                                                'PRIMDS' : dataset,
                                                'TIER' : tier1Skim.DataTier,
                                                'NODE' : tier1Skim.Node,
                                                'CMSSW' : tier1Skim.CMSSWVersion,
                                                'TWO_FILE_READ' : int(tier1Skim.TwoFileRead),
                                                'PROC_VER' : tier1Skim.ProcessingVersion,
                                                'SKIM_NAME' : tier1Skim.SkimName,
                                                'GLOBAL_TAG' : tier1Skim.GlobalTag,
                                                "CONFIG_URL" : tier1Skim.ConfigURL } )

            writeTiers = []
            if datasetConfig.Reco.WriteRECO:
                writeTiers.append("RECO")
            if datasetConfig.Reco.WriteAOD:
                writeTiers.append("AOD")
            if datasetConfig.Reco.WriteDQM:
                writeTiers.append("DQM")
            if len(datasetConfig.Reco.AlcaSkims) > 0:
                writeTiers.append("ALCARECO")

            if datasetConfig.Reco.DoReco and len(writeTiers) > 0:

                #
                # create WMSpec
                #
                taskName = "Reco"
                workflowName = "PromptReco_Run%d_%s" % (run, dataset)
                specArguments = getPromptRecoArguments()

                specArguments['AcquisitionEra'] = runInfo['acq_era']
                specArguments['CMSSWVersion'] = datasetConfig.Reco.CMSSWVersion

                specArguments['RunNumber'] = run

                specArguments['StdJobSplitArgs'] = {'events_per_job' : datasetConfig.Reco.EventSplit}

                specArguments['ProcessingString'] = "PromptReco"
                specArguments['ProcessingVersion'] = datasetConfig.Reco.ProcessingVersion
                specArguments['ProcScenario'] = datasetConfig.Scenario
                specArguments['GlobalTag'] = datasetConfig.Reco.GlobalTag

                specArguments['InputDataset'] = "/%s/%s-%s/RAW" % (dataset, runInfo['acq_era'], repackProcVer)

                specArguments['WriteTiers'] = writeTiers
                specArguments['AlcaSkims'] = datasetConfig.Reco.AlcaSkims
                specArguments['DqmSequences'] = datasetConfig.Reco.DqmSequences

                specArguments['UnmergedLFNBase'] = "%s/t0temp/%s" % (runInfo['lfn_prefix'],
                                                                     runInfo['bulk_data_type'])
                specArguments['MergedLFNBase'] = "%s/%s" % (runInfo['lfn_prefix'],
                                                            runInfo['bulk_data_type'])

                specArguments['OverrideCatalog'] = "trivialcatalog_file:/afs/cern.ch/cms/SITECONF/T0_CH_CERN/Tier0/override_catalog.xml?protocol=override"
                specArguments['ValidStatus'] = "VALID"

                specArguments['DQMUploadProxy'] = dqmUploadProxy
                specArguments['DQMUploadUrl'] = runInfo['dqmuploadurl']

                wmSpec = promptrecoWorkload(workflowName, specArguments)

                wmSpec.setPhEDExInjectionOverride(runInfo['bulk_data_loc'])
                for subscription in subscriptions:
                    wmSpec.setSubscriptionInformation(**subscription)

                wmSpec.setOwnerDetails("Dirk.Hufnagel@cern.ch", "T0",
                                       { 'vogroup': 'DEFAULT', 'vorole': 'DEFAULT',
                                         'dn' : "Dirk.Hufnagel@cern.ch" } )

                wmSpec.setupPerformanceMonitoring(maxRSS = 10485760, maxVSize = 10485760,
                                                  softTimeout = 604800, gracePeriod = 3600)

                wmbsHelper = WMBSHelper(wmSpec, taskName, cachepath = specDirectory)

                recoSpecs[workflowName] = (wmbsHelper, wmSpec, fileset)

    try:
        myThread.transaction.begin()
        if len(bindsDatasetScenario) > 0:
            insertDatasetScenarioDAO.execute(bindsDatasetScenario, conn = myThread.transaction.conn, transaction = True)
        if len(bindsCMSSWVersion) > 0:
            insertCMSSWVersionDAO.execute(bindsCMSSWVersion, conn = myThread.transaction.conn, transaction = True)
        if len(bindsRecoConfig) > 0:
            insertRecoConfigDAO.execute(bindsRecoConfig, conn = myThread.transaction.conn, transaction = True)
        if len(bindsStorageNode) > 0:
            insertStorageNodeDAO.execute(bindsStorageNode, conn = myThread.transaction.conn, transaction = True)
        if len(bindsPromptSkimConfig) > 0:
            insertPromptSkimConfigDAO.execute(bindsPromptSkimConfig, conn = myThread.transaction.conn, transaction = True)
        if len(bindsReleasePromptReco) > 0:
            releasePromptRecoDAO.execute(bindsReleasePromptReco, conn = myThread.transaction.conn, transaction = True)
        for (wmbsHelper, wmSpec, fileset) in recoSpecs.values():
            wmbsHelper.createSubscription(wmSpec.getTask(taskName), Fileset(id = fileset), alternativeFilesetClose = True)
            insertWorkflowMonitoringDAO.execute([fileset],  conn = myThread.transaction.conn, transaction = True)
        if len(recoSpecs) > 0:
            markWorkflowsInjectedDAO.execute(recoSpecs.keys(), injected = True, conn = myThread.transaction.conn, transaction = True)
    except:
        myThread.transaction.rollback()
        raise
    else:
        myThread.transaction.commit()

    return
