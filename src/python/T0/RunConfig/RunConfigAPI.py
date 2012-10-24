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
            updateRunDAO.execute(bindsUpdateRun,
                                 transaction = True)
            insertStreamDAO.execute(bindsStream,
                                    transaction = True)
            insertDatasetDAO.execute(bindsDataset,
                                     transaction = True)
            insertStreamDatasetDAO.execute(bindsStreamDataset,
                                           transaction = True)
            insertTriggerDAO.execute(bindsTrigger,
                                     transaction = True)
            insertDatasetTriggerDAO.execute(bindsDatasetTrigger,
                                            transaction = True)
        except:
            myThread.transaction.rollback()
            raise
        else:
            myThread.transaction.commit()

    else:

        try:
            myThread.transaction.begin()
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
            updateRunDAO.execute(bindsUpdateRun,
                                 transaction = True)
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
        insertErrorDatasetDAO = daoFactory(classname = "RunConfig.InsertErrorDataset")
        insertStreamFilesetDAO = daoFactory(classname = "RunConfig.InsertStreamFileset")
        insertRecoReleaseConfigDAO = daoFactory(classname = "RunConfig.InsertRecoReleaseConfig")
        insertWorkflowMonitoringDAO = daoFactory(classname = "RunConfig.InsertWorkflowMonitoring")

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
        bindsErrorDataset = []

        # mark workflows as injected
        wmbsDaoFactory = DAOFactory(package = "WMCore.WMBS",
                                    logger = logging,
                                    dbinterface = myThread.dbi)
        markWorkflowsInjectedDAO   = wmbsDaoFactory(classname = "Workflow.MarkInjectedWorkflows")

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
        # first take care of all stream settings
        #
        getStreamOnlineVersionDAO = daoFactory(classname = "RunConfig.GetStreamOnlineVersion")
        onlineVersion = getStreamOnlineVersionDAO.execute(run, stream, transaction = False)

        if streamConfig.ProcessingStyle == "Bulk":

            bindsRepackConfig = { 'RUN' : run,
                                  'STREAM' : stream,
                                  'PROC_VER': streamConfig.Repack.ProcessingVersion }

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
                                   'ALCA_SKIM' : alcaSkim,
                                   'DQM_SEQ' : dqmSeq,
                                   'GLOBAL_TAG' : streamConfig.Express.GlobalTag }


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

            datasetConfig = retrieveDatasetConfig(tier0Config, dataset)

            promptRecoDelay[datasetConfig.Name] = datasetConfig.RecoDelay
            promptRecoDelayOffset[datasetConfig.Name] = datasetConfig.RecoDelayOffset

            selectEvents = []
            for path in sorted(paths):
                selectEvents.append("%s:%s" % (path, runInfo['process']))

            if streamConfig.ProcessingStyle == "Bulk":

                outputModuleDetails.append( { 'dataTier' : "RAW",
                                              'eventContent' : "ALL",
                                              'selectEvents' : selectEvents,
                                              'primaryDataset' : datasetConfig.Name } )

##                 errorDataset = "%s-%s" % (dataset, "Error")
##                 bindsDataset.append( { 'PRIMDS' : errorDataset } )
##                 bindsStreamDataset.append( { 'RUN' : run,
##                                              'PRIMDS' : errorDataset,
##                                              'STREAM' : stream } )
##                 bindsErrorDataset.append( { 'PARENT' : dataset,
##                                             'ERROR' : errorDataset } )

            elif streamConfig.ProcessingStyle == "Express":

                for dataTier in streamConfig.Express.DataTiers:
                    if dataTier not in [ "ALCARECO", "DQM" ]:
                        outputModuleDetails.append( { 'dataTier' : dataTier,
                                                      'eventContent' : dataTier,
                                                      'selectEvents' : selectEvents,
                                                      'primaryDataset' : datasetConfig.Name } )

                #insertPhEDExConfig(dbConn, runNumber, dataset,
                #                   None, "T2_CH_CAF", None, False)

                #insertPhEDExConfig(dbConn, runNumber, errorDataset,
                #                   None, "T2_CH_CAF", None, False)




        #
        # finally create WMSpec
        #
        outputs = {}
        if streamConfig.ProcessingStyle == "Bulk":
            taskName = "Repack"
            workflowName = "Repack_Run%d_Stream%s" % (run, stream)
            specArguments = getRepackArguments()
            specArguments['ProcessingVersion'] = streamConfig.Repack.ProcessingVersion
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
            specArguments['AlcaSkims'] = streamConfig.Express.AlcaSkims
            specArguments['DqmSequences'] = streamConfig.Express.DqmSequences
            specArguments['UnmergedLFNBase'] = "%s/t0temp/express" % runInfo['lfn_prefix']
            specArguments['MergedLFNBase'] = "%s/express" % runInfo['lfn_prefix']
            specArguments['AlcaHarvestTimeout'] = runInfo['ah_timeout']
            specArguments['AlcaHarvestDir'] = runInfo['ah_dir']
            specArguments['DQMUploadProxy'] = dqmUploadProxy
            specArguments['StreamName'] = stream

        if streamConfig.ProcessingStyle in [ 'Bulk', 'Express' ]:
            specArguments['RunNumber'] = run
            specArguments['AcquisitionEra'] = tier0Config.Global.AcquisitionEra
            specArguments['CMSSWVersion'] = streamConfig.VersionOverride.get(onlineVersion, onlineVersion)
            specArguments['Outputs'] = outputModuleDetails
            specArguments['OverrideCatalog'] = "trivialcatalog_file:/afs/cern.ch/cms/SITECONF/local/Tier0/override_catalog.xml?protocol=override"

        if streamConfig.ProcessingStyle == "Bulk":
            wmSpec = repackWorkload(workflowName, specArguments)
        elif streamConfig.ProcessingStyle == "Express":
            wmSpec = expressWorkload(workflowName, specArguments)

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
            if len(bindsErrorDataset) > 0:
                insertErrorDatasetDAO.execute(bindsErrorDataset, conn = myThread.transaction.conn, transaction = True)
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
    bindsPhEDExConfig = []
    bindsPromptSkimConfig = []
    bindsReleasePromptReco = []

    # mark workflows as injected
    wmbsDaoFactory = DAOFactory(package = "WMCore.WMBS",
                                logger = logging,
                                dbinterface = myThread.dbi)
    markWorkflowsInjectedDAO   = wmbsDaoFactory(classname = "Workflow.MarkInjectedWorkflows")

    recoSpecs = {}

    findRecoReleaseDAO = daoFactory(classname = "RunConfig.FindRecoRelease")
    recoRelease = findRecoReleaseDAO.execute(transaction = False)

    for run in sorted(recoRelease.keys()):

        # retrieve some basic run information
        getRunInfoDAO = daoFactory(classname = "RunConfig.GetRunInfo")
        runInfo = getRunInfoDAO.execute(run, transaction = False)[0]

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

            requestOnly = "y"
            if datasetConfig.CustodialAutoApprove:
                requestOnly = "n"

            if datasetConfig.CustodialNode != None:

                bindsStorageNode.append( { 'NODE' : datasetConfig.CustodialNode } )

                bindsPhEDExConfig.append( { 'RUN' : run,
                                            'PRIMDS' : dataset,
                                            'NODE' : datasetConfig.CustodialNode,
                                            'CUSTODIAL' : 1,
                                            'REQ_ONLY' : requestOnly,
                                            'PRIO' : datasetConfig.CustodialPriority } )

            if datasetConfig.ArchivalNode != None:

                bindsStorageNode.append( { 'NODE' : datasetConfig.ArchivalNode } )

                bindsPhEDExConfig.append( { 'RUN' : run,
                                            'PRIMDS' : dataset,
                                            'NODE' : datasetConfig.ArchivalNode,
                                            'CUSTODIAL' : 0,
                                            'REQ_ONLY' : "n",
                                            'PRIO' : "high" } )

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

                specArguments['OverrideCatalog'] = "trivialcatalog_file:/afs/cern.ch/cms/SITECONF/local/Tier0/override_catalog.xml?protocol=override"
                specArguments['DQMUploadProxy'] = dqmUploadProxy

                specArguments['DoLogCollect'] = False

                wmSpec = promptrecoWorkload(workflowName, specArguments)

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
        if len(bindsPhEDExConfig) > 0:
            insertPhEDExConfigDAO.execute(bindsPhEDExConfig, conn = myThread.transaction.conn, transaction = True)
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
