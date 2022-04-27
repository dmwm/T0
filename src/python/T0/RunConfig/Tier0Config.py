"""
_Tier0Config_

Utility methods for creating and manipulating a Tier0 configuration

The Tier0 configuration has the following form:

Tier0Configuration - Global configuration object
| | | |--> Sites - Configuration parameter for sites that are going
| | |        |     to be use for processing and storage
| | |        |
| | |        |--> OverrideCatalog - Path to this site's trivial catalog file
| | |        |
| | |        |--> SiteLocalConfig - Path to this site's site local config file
| | |
| | |--> Global - Configuration parameters that do not belong to a particular
| |       |       stream or dataset and can be applied to an entire run.
| |       |
| |       |--> Version - The configuration version (not used at the moment)
| |       |
| |       |--> InjectRuns - The runs to be injected into the system from the SM database (default is auto-discovery)
| |       |
| |       |--> InjectMinRun - Lowest run number to be injected into the system from the SM database (default is unlimited)
| |       |
| |       |--> InjectMaxRun - Highest run number to be injected into the system from the SM database (default is unlimited)
| |       |
| |       |--> AcquisitionEra - The acquisition era for the run
| |       |
| |       |--> Backfill - The backfill mode, can be None, 1 or 2
| |       |
| |       |--> ProcessingSite - Main (CERN) site where processing is done.
| |       |
| |       |--> StreamerPNN - PNN where streamer file are located
| |       |
| |       |--> BulkDataType - The bulk data type for the run
| |       |
| |       |--> DQMDataTier - The data tier used for DQM (default is DQMIO).
| |       |
| |       |--> DQMUploadURL - The URL used for DQM uploads
| |       |
| |       |--> AlcaHarvestTimeout - AlcaHarvesting for a run/stream is normally trigered by
| |       |                         fileset closing (ie. all data received and processed).
| |       |                         This timeout will configure an additional time trigger
| |       |                         based on the run stop_time.
| |       |
| |       |--> AlcaHarvestCondLFNBase - LFNBase to which the AlcaHarvest job copies the
| |       |                             sqlite file and associated metadata.
| |       |
| |       |--> AlcaHarvestLumiURL - URL to which the AlcaHarvest job copies the
| |       |                         lumi text file for the LHC.
| |       |
| |       |--> ConditionUploadTimeout - ConditionUpload normally only advances to the next run
| |       |                             if the current run is completely finished (ie. all data
| |       |                             received, processed, alca harvested and conditions
| |       |                             uploaded). This timeout will configure an additional
| |       |                             time trigger based on the run stop_time.
| |       |
| |       |--> DropBoxHost - Machine where we upload the PCL conditions to
| |       |
| |       |--> ValidationMode - Whether or not we upload conditions for immediate use
| |       |                     in PromptReco or just for validation checks.
| |       |
| |       |--> ScramArches - Dictionary containig CMSSW release and corresponding ScramArch
| |       |
| |       |--> DefaultScramArch - Default ScramArch if nothing else is specified for release
| |       |
| |       |--> BaseRequestPriority - Base for request priorities for PromptReco/Repack/Express
| |       |
| |       |--> DeploymentID - Unique identifier for every T0 Agent deployment
| |
| |
| |--> Streams - Configuration parameters that belong to a particular stream
|       |
|       | |--> Default - Configuration section for repacking defaults
|       |                (configured just like a repack stream)
|       |      
|       |--> STREAMNAME - Configuration section for a stream.
|             |
|             |--> ProcessingStyle - The processing style for the stream
|             |
|             |--> VersionOverride - Override mapping for CMSSW versions
|             |
|             |--> Repack - Configuration section for bulk streams
|             |     |
|             |     |--> ProcessingVersion - processing version
|             |     |
|             |     |--> MaxSizeSingleLumi - max size of single lumi before we break
|             |     |                        it up into multiple repack jobs
|             |     |
|             |     |--> MaxSizeMultiLumi - max size for a multi lumi repack job
|             |     |
|             |     |--> MinInputSize - min input size for repack merge job
|             |     |
|             |     |--> MaxInputSize - max input size for repack merge job
|             |     |
|             |     |--> MaxEdmSize - max size for repack merge output, break
|             |     |                 up lumi into multiple files and send to
|             |     |                 error dataset if larger
|             |     |
|             |     |--> MaxOverSize - max size for overmerge (where merging in
|             |     |                  order forces us to use a lumi to get over
|             |     |                  the min size but that also gets us over
|             |     |                  the max size allowed. In these case we
|             |     |                  have a preference for creating too large
|             |     |                  files compared to too small files.
|             |     |
|             |     |--> MaxInputEvents - max input events for repack and repack merge job
|             |     |
|             |     |--> MaxInputFiles - max input files for repack and repack merge job
|             |     |
|             |     |--> MaxLatency - max latency to trigger repack or repack merge job
|             |     |
|             |     |--> BlockCloseDelay - delay to close block in WMAgent
|             |
|             |--> Express - Configuration section for express streams
|             |     |
|             |     |--> Scenario - Event scenario, determines configurations used
|             |     |
|             |     |--> DataTiers - List of data tiers
|             |     |
|             |     |--> GlobalTag - Global tag used for processing
|             |     |
|             |     |--> RecoCMSSWVersion - Framework version used for processing. This only
|             |     |                       needs to be filled if we want to run the reco
|             |     |                       step separate from the repacking step.
|             |     |
|             |     |--> Multicore - number of cores to be used for the reco step (optional)
|             |     |
|             |     |--> AlcaSkims - List of alca skims active for this stream.
|             |     |
|             |     |--> WriteDQM - whether we write out DQM information
|             |     |
|             |     |--> DqmSequences - List of dqm sequences active for this stream.
|             |     |
|             |     |--> ProcessingVersion - processing version
|             |     |
|             |     |--> MaxInputRate - max input rate that is accepted for processing
|             |     |                       (in events per lumi section) 
|             |     |
|             |     |--> MaxInputEvents - max input events for express processing job
|             |     |
|             |     |--> MaxInputSize - max input size for express merge job
|             |     |
|             |     |--> MaxInputFiles - max input files for express merge job
|             |     |
|             |     |--> MaxLatency - max latency to trigger express merge job
|             |     |
|             |     |--> DqmInterval - periodic DQM harvesting interval
|             |     |
|             |     |--> DataType - The type of data in this stream (default express)
|             |     |
|             |     |--> ArchivalNode - The archival PhEDEx node (default None)
|             |     |
|             |     |--> TapeNode - The tape PhEDEx node (default None)
|             |     |
|             |     |--> RAWTapeNode - The tape PhEDEx node for RAW (default None)
|             |     |
|             |     |--> DiskNode - The disk PhEDEx node (default None)
|             |     |
|             |     |--> DiskNodeReco - The disk PhEDEx node for bulk RECO data (default None)
|             |     |
|             |     |--> RAWToDisk - Do we subscribe RAW to disk?
|             |     |
|             |     |--> PhEDExGroup - The PhEDEx group for the subscriptions.
|             |     |
|             |     |--> BlockCloseDelay - delay to close block in WMAgent
|             |     |
|             |     |--> DatasetLifetime - dataset_lifetime for subscription to
|             |     |                       disk in seconds. 0 means lifetime of None
|             |
|             |--> Register - Configuration section for register streams
|             |     |
|             |     |--> PrimaryDataset - primary dataset to use
|             |     |
|             |     |--> ProcessedDataset - processed dataset to use
|             |     |
|             |     |--> DataTier - data tier to use
|             |
|             |--> Convert - Configuration section for convert streams
|                   |
|                   |--> PrimaryDataset - primary dataset for output
|                   |
|                   |--> ProcessedDataset - processed dataset for output
|                   |
|                   |--> DataTier - data tier to use
|                   |
|                   |--> Type - type of conversion (streamer, pixdmp etc)
|                   |
|                   |--> AcqEra - acquisiton era for output
|                   |
|                   |--> ProcVers - processing version for output
|                   |
|                   |--> ProcString - processing string for output
|
|--> Datasets
      | |
      | |--> Default - Configuration section to hold the default dataset config
      |                This will have the same structure as the dataset config below
      |
      |--> DATASETNAME
            |
            |--> Name - Name of the dataset
            |
            |--> Scenario - Processing scenario for this dataset
            |
            |--> RecoDelay - PromptReco delay
            |
            |--> RecoDelayOffset - Time before PromptReco is released for which
            |                      settings are locked in and reco looks released
            |
            |--> ArchivalNode - The archival PhEDEx node (should always be CERN T0)
            |
            |--> TapeNode - The tape PhEDEx node (should be T1 _MSS)
            |
            |--> DiskNode - The disk PhEDEx node (should be T1 _Disk)
            |
            |--> ProcessingVersion - Used for all output from PromptReco
            |
            |--> DoReco - Whether we are running PromptReco at all
            |
            |--> CMSSWVersion - CMSSW used for PromptReco (mandatory if DoReco is True)
            |
            |--> Multicore - number of cores to be used for the reco step (optional)
            |
            |--> GlobalTag - Global tag used for PromptReco (mandatory if DoReco is True)
            |
            |--> AlcaSkims - List of alca skims active for this dataset
            |
            |--> PhysicsSkims - List of physics skims active for this dataset
            |
            |--> DqmSequences - List of dqm sequences active for this dataset
            |
            |--> BlockCloseDelay - Delay to close block in WMAgent
            |
            |--> SiteWhitelist - Site whitelist for PromptReco
            |
            |--> DatasetLifetime - dataset_lifetime for subscription to disk in
                                    seconds. 0 means lifetime of None
"""

import logging
import copy

from WMCore.Configuration import Configuration
from WMCore.Configuration import ConfigSection

def createTier0Config():
    """
    _createTier0Config_

    Create a configuration object to hold the Tier0 configuration.  Currently,
    the configuration has two sections: Streams and Global.
    """
    tier0Config = Configuration()
    tier0Config.section_("Streams")
    tier0Config.section_("Datasets")
    tier0Config.section_("Sites")
    tier0Config.section_("Global")

    tier0Config.Global.InjectRuns = None
    tier0Config.Global.InjectMinRun = None
    tier0Config.Global.InjectMaxRun = None

    tier0Config.Global.ScramArches = {}
    tier0Config.Global.Backfill = None

    tier0Config.Global.ProcessingSite = "T2_CH_CERN"

    tier0Config.Global.StreamerPNN = "T0_CH_CERN_Disk"

    tier0Config.Global.StorageSite = "T0_CH_CERN_Disk"

    tier0Config.Global.DQMDataTier = "DQMIO"

    tier0Config.Global.BaseRequestPriority = 150000

    tier0Config.Global.EnableUniqueWorkflowName = False

    tier0Config.Global.DeploymentID = 1

    return tier0Config

def retrieveStreamConfig(config, streamName):
    """
    _retrieveStreamConfig_
    
    Lookup the configuration for the given stream.  If the configuration for a
    particular stream is not explicitly defined, return the default configuration.
    """
    streamConfig = getattr(config.Streams, streamName, None)
    if streamConfig == None:

        defaultInstance = getattr(config.Streams, "Default", None)

        if defaultInstance == None:
            streamConfig = config.Streams.section_(streamName)
        else:
            streamConfig = copy.deepcopy(defaultInstance)
            streamConfig._internal_name = streamName
            streamConfig.Name = streamName
            setattr(config.Streams, streamName, streamConfig)

    return streamConfig

def deleteStreamConfig(config, streamName):
    """
    _deleteStreamConfig_
    
    Removes a stream configuration
    """
    streamConfig =  getattr(config.Streams, streamName, None)
    if streamConfig != None:
        delattr(config.Streams, streamName)

    return

def retrieveSiteConfig(config, siteName):
    """
    _retrieveSiteConfig_
    
    Lookup the configuration for the given site.  If the configuration for a
    particular site is not explicitly defined, return the default configuration.
    """
    siteConfig = getattr(config.Sites, siteName, None)
    if siteConfig == None:

        defaultInstance = getattr(config.Sites, "Default", None)

        if defaultInstance == None:
            siteConfig = config.Sites.section_(siteName)
        else:
            siteConfig = copy.deepcopy(defaultInstance)
            siteConfig._internal_name = siteName
            siteConfig.Name = siteName
            setattr(config.Sites, siteName, siteConfig)

    return siteConfig

def deleteSiteConfig(config, siteName):
    """
    _deleteSiteConfig_
    
    Removes a site configuration
    """
    siteConfig =  getattr(config.Sites, siteName, None)
    if siteConfig != None:
        delattr(config.Sites, siteName)

    return

def retrieveDatasetConfig(config, datasetName, fromAddDataset = False):
    """
    _retrieveDatasetConfig_
    
    Lookup the configuration for the given dataset.  If the configuration for a
    particular dataset is not defined return the default configuration.
    """
    datasetConfig = getattr(config.Datasets, datasetName, None)

    if datasetConfig == None:
        defaultInstance = getattr(config.Datasets, "Default", None)
        if defaultInstance == None:
            datasetConfig = config.Datasets.section_(datasetName)
        else:
            datasetConfig = copy.deepcopy(defaultInstance)
            datasetConfig._internal_name = datasetName
            datasetConfig.Name = datasetName
            setattr(config.Datasets, datasetName, datasetConfig)
    elif fromAddDataset:
        # don't allow multiple addDataset calls for the same dataset
        msg = "Tier0Config.addDataset : multiple addDataset calls for dataset %s not allowed" % datasetName
        raise RuntimeError(msg)

    return datasetConfig


def addDataset(config, datasetName, **settings):
    """
    _addDataset_

    Add a dataset to the configuration using settings from either
    explictely define parameters or using the ones from the
    Default dataset (not all parameters can be overridden).

    The following keys may be passed
      scenario - the processing scenario
      do_reco - whether we run PromptReco at all
      reco_delay - time to wait for PromptReco release
      reco_delay_offset - time shift before PromptReco release
                          when that release is locked in
      proc_version - processing version for all outputs
      cmssw_version - framework version
      global_tag - the global tag to use
      global_tag_connect - connect straing for global tag
      reco_split - number of events to process per reco job
      write_reco - whether the reco jobs writes RECO output
      write_aod - whether the reco job writes AOD output
      write_miniaod - whether the reco job writes MINIAOD output
      write_dqm - whether the reco job writes DQM output
      archival_node - PhEDEx archival node for this dataset
                      (defaults to None)
      alca_producers - alca producers for reco, be be split
                       out into separate sampls in alca skimming
                       (defaults to empty list)
      dqm_sequences - dqm sequences used for reco
                      (defaults to empty list) 
      custodial_node - PhEDEx custodial node for this dataset
      custodial_priority - priority for the custodial subscription
                           (defaults to high)
      custodial_auto_approve - auto-approve the custodial subscription
                               (defaults to False)
      blockCloseDelay - block closing timeout in hours
    """
    datasetConfig = retrieveDatasetConfig(config, datasetName, True)

    #
    # first the mandatory paramters
    #
    # they can either be set for Default or directly for the dataset
    #
    if 'scenario' in settings:
        datasetConfig.Scenario = settings['scenario']
    if not hasattr(datasetConfig, "Scenario") or not (isinstance(datasetConfig.Scenario, str) or isinstance(datasetConfig.Scenario, dict)):
        msg = "Tier0Config.addDataset : no valid scenario defined for dataset %s or Default" % datasetName
        raise RuntimeError(msg)

    if 'do_reco' in settings:
        datasetConfig.DoReco = settings['do_reco']
    if not hasattr(datasetConfig, "DoReco") or not isinstance(datasetConfig.DoReco, bool):
        msg = "Tier0Config.addDataset : no valid do_reco defined for dataset %s or Default" % datasetName
        raise RuntimeError(msg)

    if 'reco_delay' in settings:
        datasetConfig.RecoDelay = settings['reco_delay']
    if not hasattr(datasetConfig, "RecoDelay") or not isinstance(datasetConfig.RecoDelay, int):
        msg = "Tier0Config.addDataset : no valid reco_delay defined for dataset %s or Default" % datasetName
        raise RuntimeError(msg)

    if 'reco_delay_offset' in settings:
        datasetConfig.RecoDelayOffset = settings['reco_delay_offset']
    if not hasattr(datasetConfig, "RecoDelayOffset") or not isinstance(datasetConfig.RecoDelayOffset, int):
        msg = "Tier0Config.addDataset : no valid reco_delay_offset defined for dataset %s or Default" % datasetName
        raise RuntimeError(msg)

    if 'proc_version' in settings:
        datasetConfig.ProcessingVersion = settings['proc_version']
    if not hasattr(datasetConfig, "ProcessingVersion") or not (isinstance(datasetConfig.ProcessingVersion, int) or isinstance(datasetConfig.ProcessingVersion, dict)):
        msg = "Tier0Config.addDataset : no valid proc_version defined for dataset %s or Default" % datasetName
        raise RuntimeError(msg)

    if 'cmssw_version' in settings:
        datasetConfig.CMSSWVersion = settings['cmssw_version']
    if not hasattr(datasetConfig, "CMSSWVersion") or not (isinstance(datasetConfig.CMSSWVersion, str) or isinstance(datasetConfig.CMSSWVersion, dict)):
        msg = "Tier0Config.addDataset : no valid cmssw_version defined for dataset %s or Default" % datasetName
        raise RuntimeError(msg)

    if 'global_tag' in settings:
        datasetConfig.GlobalTag = settings['global_tag']
    if not hasattr(datasetConfig, "GlobalTag") or not (isinstance(datasetConfig.GlobalTag, str) or isinstance(datasetConfig.GlobalTag, dict)):
        msg = "Tier0Config.addDataset : no valid global_tag defined for dataset %s or Default" % datasetName
        raise RuntimeError(msg)

    if 'reco_split' in settings:
        datasetConfig.RecoSplit = settings['reco_split']
    if not hasattr(datasetConfig, "RecoSplit") or not isinstance(datasetConfig.RecoSplit, int):
        msg = "Tier0Config.addDataset : no valid reco_split defined for dataset %s or Default" % datasetName
        raise RuntimeError(msg)

    if 'write_reco' in settings:
        datasetConfig.WriteRECO = settings['write_reco']
    if not hasattr(datasetConfig, "WriteRECO") or not isinstance(datasetConfig.WriteRECO, bool):
        msg = "Tier0Config.addDataset : no valid write_reco defined for dataset %s or Default" % datasetName
        raise RuntimeError(msg)

    if 'write_aod' in settings:
        datasetConfig.WriteAOD = settings['write_aod']
    if not hasattr(datasetConfig, "WriteAOD") or not isinstance(datasetConfig.WriteAOD, bool):
        msg = "Tier0Config.addDataset : no valid write_aod defined for dataset %s or Default" % datasetName
        raise RuntimeError(msg)

    if 'write_miniaod' in settings:
        datasetConfig.WriteMINIAOD = settings['write_miniaod']
    if not hasattr(datasetConfig, "WriteMINIAOD") or not isinstance(datasetConfig.WriteMINIAOD, bool):
        msg = "Tier0Config.addDataset : no valid write_miniaod defined for dataset %s or Default" % datasetName
        raise RuntimeError(msg)

    if 'write_dqm' in settings:
        datasetConfig.WriteDQM = settings['write_dqm']
    if not hasattr(datasetConfig, "WriteDQM") or not isinstance(datasetConfig.WriteDQM, bool):
        msg = "Tier0Config.addDataset : no valid write_dqm defined for dataset %s or Default" % datasetName
        raise RuntimeError(msg)

    if 'timePerEvent' in settings:
        datasetConfig.TimePerEvent = settings['timePerEvent']
    if not hasattr(datasetConfig, "TimePerEvent") or not (isinstance(datasetConfig.TimePerEvent, int) or isinstance(datasetConfig.TimePerEvent, float)):
        msg = "Tier0Config.addDataset : no valid timePerEvent defined for dataset %s or Default" % datasetName
        raise RuntimeError(msg)

    if 'sizePerEvent' in settings:
        datasetConfig.SizePerEvent = settings['sizePerEvent']
    if not hasattr(datasetConfig, "SizePerEvent") or not (isinstance(datasetConfig.SizePerEvent, int) or isinstance(datasetConfig.SizePerEvent, float)):
        msg = "Tier0Config.addDataset : no valid sizePerEvent defined for dataset %s or Default" % datasetName
        raise RuntimeError(msg)

    if hasattr(datasetConfig, "GlobalTagConnect"):
        datasetConfig.GlobalTagConnect = settings.get('global_tag_connect', datasetConfig.GlobalTagConnect)
    else:
        datasetConfig.GlobalTagConnect = settings.get('global_tag_connect', None)

    if hasattr(datasetConfig, "ArchivalNode"):
        datasetConfig.ArchivalNode = settings.get('archival_node', datasetConfig.ArchivalNode)
    else:
        datasetConfig.ArchivalNode = settings.get('archival_node', None)

    if hasattr(datasetConfig, "TapeNode"):
        datasetConfig.TapeNode = settings.get('tape_node', datasetConfig.TapeNode)
    else:
        datasetConfig.TapeNode = settings.get('tape_node', None)

    if hasattr(datasetConfig, "RAWTapeNode"):
        datasetConfig.RAWTapeNode = settings.get('raw_tape_node', datasetConfig.RAWTapeNode)
    else:
        datasetConfig.RAWTapeNode = settings.get('raw_tape_node', None)

    if hasattr(datasetConfig, "DiskNode"):
        datasetConfig.DiskNode = settings.get('disk_node', datasetConfig.DiskNode)
    else:
        datasetConfig.DiskNode = settings.get('disk_node', None)

    if hasattr(datasetConfig, "DiskNodeReco"):
        datasetConfig.DiskNodeReco = settings.get('disk_node_reco', datasetConfig.DiskNodeReco)
    else:
        datasetConfig.DiskNodeReco = settings.get('disk_node_reco', None)

    if hasattr(datasetConfig, "RAWtoDisk"):
        datasetConfig.RAWtoDisk = settings.get('raw_to_disk', datasetConfig.RAWtoDisk)
    else:
        datasetConfig.RAWtoDisk = settings.get('raw_to_disk', True)

    if hasattr(datasetConfig, "Multicore"):
        datasetConfig.Multicore = settings.get('multicore', datasetConfig.Multicore)
    else:
        datasetConfig.Multicore = settings.get('multicore', None)

    #
    # optional parameter, Default rule is still used
    #
    if hasattr(datasetConfig, "BlockCloseDelay"):
        datasetConfig.BlockCloseDelay = settings.get("blockCloseDelay", datasetConfig.BlockCloseDelay)
    else:
        datasetConfig.BlockCloseDelay = settings.get("blockCloseDelay", 24 * 3600)

    if hasattr(datasetConfig, "SiteWhitelist"):
        datasetConfig.SiteWhitelist = settings.get("siteWhitelist", datasetConfig.SiteWhitelist)
    else:
        datasetConfig.SiteWhitelist = settings.get("siteWhitelist", [ config.Global.ProcessingSite ])

    #
    # finally some parameters for which Default isn't used
    #
    datasetConfig.AlcaSkims = settings.get("alca_producers", [])
    datasetConfig.PhysicsSkims = settings.get("physics_skims", [])
    datasetConfig.DqmSequences = settings.get("dqm_sequences", [])

    if hasattr(datasetConfig, "MaxMemoryperCore"):
        datasetConfig.MaxMemoryperCore = settings.get("maxMemoryperCore", datasetConfig.MaxMemoryperCore)
    else:
        datasetConfig.MaxMemoryperCore = settings.get("maxMemoryperCore", 2000)

    if hasattr(datasetConfig, "datasetLifetime"):
        datasetConfig.datasetLifetime = settings.get("dataset_lifetime", datasetConfig.datasetLifetime)
    else:
        datasetConfig.datasetLifetime = settings.get("dataset_lifetime", 0)

    return

def setAcquisitionEra(config, acquisitionEra):
    """
    _setAcquisitionEra_

    Set the acquisition era in the configuration.
    """
    config.Global.AcquisitionEra = acquisitionEra
    return

def setScramArch(config, cmssw, arch):
    """
    _setDefaultScramArch_

    Set the default scram arch in this configuration.
    """
    config.Global.ScramArches[cmssw] = arch
    return

def setBaseRequestPriority(config, priority):
    """
    _setBaseRequestPriority_

    Set the base request priority.
    """
    config.Global.BaseRequestPriority = priority
    return

def setDefaultScramArch(config, arch):
    """
    _setDefaultScramArch_

    Set the default scram arch in this configuration.
    """
    config.Global.DefaultScramArch = arch
    return

def setBackfill(config, mode):
    """
    _setBackfill_

    Set the backfill mode in the configuration.
    """
    if mode not in [ None, 1, 2, 3 ]:
        msg = "Tier0Config.setBackfill : %s is not a valid backfill mode" % mode
        raise RuntimeError(msg)

    config.Global.Backfill = mode
    return

def setProcessingSite(config, site):
    """
    _setProcessingSite_

    Set the (CERN) site used for processing.
    """
    config.Global.ProcessingSite = site
    return

def setStorageSite(config, site):
    """
    _setStorageSite_

    Set the (CERN) site used for disk storage.
    """
    config.Global.StorageSite = site
    return

def setStreamerPNN(config, pnn):
    """
    _setStreamerPNN_

    Set the (CERN) location for streamer files.
    """
    config.Global.StreamerPNN = pnn
    return

def setOverrideCatalog(config, overrideCatalog):
    """
    _setOverrideCatalog_

    Set the catalog to use in case override is necessary.
    """
    config.Global.overrideCatalog = overrideCatalog
    return


def setSiteLocalConfig(config, siteLocalConfig):
    """
    _setSiteLocalConfig_

    Set the site local config file to use in case override is necessary.
    """
    config.Global.siteLocalConfig = siteLocalConfig
    return

def setBulkDataType(config, type):
    """
    _setBulkDataType_

    Set the bulk data type in the configuration.
    """
    config.Global.BulkDataType = type
    return

def setDQMDataTier(config, datatier):
    """
    _setDQMDataTier_

    Set the DQM data tier

    """
    if datatier not in [ "DQM", "DQMIO" ]:
        msg = "Tier0Config.setDQMDataTier : %s not an allowed DQM data tier !" % datatier
        raise RuntimeError(msg)

    config.Global.DQMDataTier = datatier
    return

def setDQMUploadUrl(config, dqmuploadurl):
    """
    _setDQMUploadUrl_

    Set the DQM upload Url in the configuration.
    
    """
    config.Global.DQMUploadUrl = dqmuploadurl
    return

def setPromptCalibrationConfig(config, alcaHarvestTimeout,
                               alcaHarvestCondLFNBase, alcaHarvestLumiURL,
                               conditionUploadTimeout, dropboxHost,
                               validationMode):
    """
    _setPromptCalibrationConfig_

    Configure needed settings for PromptCalibration
    """
    config.Global.AlcaHarvestTimeout = alcaHarvestTimeout
    config.Global.AlcaHarvestCondLFNBase = alcaHarvestCondLFNBase
    config.Global.AlcaHarvestLumiURL = alcaHarvestLumiURL
    config.Global.ConditionUploadTimeout = conditionUploadTimeout
    config.Global.DropboxHost = dropboxHost
    config.Global.ValidationMode = validationMode
    return

def setConfigVersion(config, version):
    """
    _setConfigVersion_

    Set the version of the config.  This will more than likely be the CVS
    revision of the configuration.
    """
    config.Global.Version = version
    return

def setInjectRuns(config, injectRuns):
    """
    _setInjectRuns_

    Set the runs to be injected into the Tier0.
    """
    config.Global.InjectRuns = injectRuns
    return

def setInjectMinRun(config, injectMinRun):
    """
    _setInjectMinRun_

    Set the lowest run to be injected into the Tier0.
    """
    config.Global.InjectMinRun = injectMinRun
    return

def setInjectMaxRun(config, injectMaxRun):
    """
    _setInjectMaxRun_

    Set the highest run to be injected into the Tier0.
    """
    config.Global.InjectMaxRun = injectMaxRun
    return

def setEnableUniqueWorkflowName(config):
    """
    _setEnableUniqueWorkflowName_

    Enables using unique workflow names in Tier0 replays.
    Uses era name, Repack, Express, PromptReco processing versions, date/time, e.g.:
    PromptReco_Run322057_Charmonium_Tier0_REPLAY_vocms047_v274_190221_121
    """
    config.Global.EnableUniqueWorkflowName = True
    return

def setDeploymentId(config, id):
    """
    _setDeploymentId_

    Sets an ID for the current deployment of T0
    """
    config.Global.DeploymentID = id
    return

def ignoreStream(config, streamName):
    """
    _ignoreStream_

    adds a configuration for a stream that
    sets it to be ignored
    """
    streamConfig = retrieveStreamConfig(config, streamName)
    streamConfig.ProcessingStyle = "Ignore"

    return

def addRepackConfig(config, streamName, **options):
    """
    _addRepackConfig_

    Add an repack configuration to a given stream.

    At the moment more a placeholder, only contains
    the dynamically applied version override.

    """
    streamConfig = retrieveStreamConfig(config, streamName)
    streamConfig.ProcessingStyle = "Bulk"

    if hasattr(streamConfig, "VersionOverride"):
        streamConfig.VersionOverride = options.get("versionOverride", streamConfig.VersionOverride)
    else:
        streamConfig.VersionOverride = options.get("versionOverride", {})

    streamConfig.section_("Repack")

    if hasattr(streamConfig.Repack, "ProcessingVersion"):
        streamConfig.Repack.ProcessingVersion = options.get("proc_ver", streamConfig.Repack.ProcessingVersion)
    else:
        streamConfig.Repack.ProcessingVersion = options.get("proc_ver", 1)

    if hasattr(streamConfig.Repack, "MaxSizeSingleLumi"):
        streamConfig.Repack.MaxSizeSingleLumi = options.get("maxSizeSingleLumi", streamConfig.Repack.MaxSizeSingleLumi)
    else:
        streamConfig.Repack.MaxSizeSingleLumi = options.get("maxSizeSingleLumi", 10*1024*1024*1024)

    if hasattr(streamConfig.Repack, "MaxSizeMultiLumi"):
        streamConfig.Repack.MaxSizeMultiLumi = options.get("maxSizeMultiLumi", streamConfig.Repack.MaxSizeMultiLumi)
    else:
        streamConfig.Repack.MaxSizeMultiLumi = options.get("maxSizeMultiLumi", 8*1024*1024*1024)

    if hasattr(streamConfig.Repack, "MinInputSize"):
        streamConfig.Repack.MinInputSize = options.get("minInputSize", streamConfig.Repack.MinInputSize)
    else:
        streamConfig.Repack.MinInputSize = options.get("minInputSize", 2.1 * 1024 * 1024 * 1024)

    if hasattr(streamConfig.Repack, "MaxInputSize"):
        streamConfig.Repack.MaxInputSize = options.get("maxInputSize", streamConfig.Repack.MaxInputSize)
    else:
        streamConfig.Repack.MaxInputSize = options.get("maxInputSize", 4 * 1024 * 1024 * 1024)

    if hasattr(streamConfig.Repack, "MaxEdmSize"):
        streamConfig.Repack.MaxEdmSize = options.get("maxEdmSize", streamConfig.Repack.MaxEdmSize)
    else:
        streamConfig.Repack.MaxEdmSize = options.get("maxEdmSize", 10 * 1024 * 1024 * 1024)

    if hasattr(streamConfig.Repack, "MaxOverSize"):
        streamConfig.Repack.MaxOverSize = options.get("maxOverSize", streamConfig.Repack.MaxOverSize)
    else:
        streamConfig.Repack.MaxOverSize = options.get("maxOverSize", 8 * 1024 * 1024 * 1024)

    if hasattr(streamConfig.Repack, "MaxInputEvents"):
        streamConfig.Repack.MaxInputEvents = options.get("maxInputEvents", streamConfig.Repack.MaxInputEvents)
    else:
        streamConfig.Repack.MaxInputEvents = options.get("maxInputEvents", 10 * 1000 * 1000)

    if hasattr(streamConfig.Repack, "MaxInputFiles"):
        streamConfig.Repack.MaxInputFiles = options.get("maxInputFiles", streamConfig.Repack.MaxInputFiles)
    else:
        streamConfig.Repack.MaxInputFiles = options.get("maxInputFiles", 1000)

    if hasattr(streamConfig.Repack, "MaxLatency"):
        streamConfig.Repack.MaxLatency = options.get("maxLatency", streamConfig.Repack.MaxLatency)
    else:
        streamConfig.Repack.MaxLatency = options.get("maxLatency", 12 * 3600)

    if streamConfig.Repack.MaxOverSize > streamConfig.Repack.MaxEdmSize:
        streamConfig.Repack.MaxOverSize = streamConfig.Repack.MaxEdmSize

    if hasattr(streamConfig.Repack, "BlockCloseDelay"):
        streamConfig.Repack.BlockCloseDelay = options.get("blockCloseDelay", streamConfig.Repack.BlockCloseDelay)
    else:
        streamConfig.Repack.BlockCloseDelay = options.get("blockCloseDelay", 24 * 3600)

    if hasattr(streamConfig.Repack, "MaxMemory"):
        streamConfig.Repack.MaxMemory = options.get("maxMemory", streamConfig.Repack.MaxMemory)
    else:
        streamConfig.Repack.MaxMemory = options.get("maxMemory", 2000)

    return

def addExpressConfig(config, streamName, **options):
    """
    _addExpressConfig_

    Add an express configuration to a given stream.

    """
    streamConfig = retrieveStreamConfig(config, streamName)
    streamConfig.ProcessingStyle = "Express"

    streamConfig.VersionOverride = options.get("versionOverride", {})

    streamConfig.section_("Express")

    scenario = options.get("scenario", None)
    if not scenario:
        msg = "Tier0Config.addExpressConfig : no scenario defined for stream %s" % streamName
        raise RuntimeError(msg)
    streamConfig.Express.Scenario = scenario

    data_tiers = options.get("data_tiers", [])
    if not isinstance(data_tiers, list):
        msg = "Tier0Config.addExpressConfig : data_tiers needs to be list (can be an empty list)"
        raise RuntimeError(msg)
    # filter out tiers that are handled differently
    for data_tier in [ "ALCARECO", "DQM", "DQMIO" ]:
        if data_tier in data_tiers:
            data_tiers.remove(data_tier)

    streamConfig.Express.DataTiers = data_tiers

    global_tag = options.get("global_tag", None)
    if not global_tag:
        msg = "Tier0Config.addExpressConfig : global_tag not defined for stream %s" % streamName
        raise RuntimeError(msg)
    streamConfig.Express.GlobalTag = global_tag

    streamConfig.Express.GlobalTagConnect = options.get("global_tag_connect", None)
    streamConfig.Express.RecoCMSSWVersion = options.get("reco_version", None)
    streamConfig.Express.Multicore = options.get('multicore', None)

    streamConfig.Express.AlcaSkims = options.get("alca_producers", [])
    streamConfig.Express.WriteDQM = options.get("write_dqm", True)
    streamConfig.Express.DqmSequences = options.get("dqm_sequences", [])
    streamConfig.Express.ProcessingVersion = options.get("proc_ver", 1)

    timePerEvent = options.get("timePerEvent", None)
    if timePerEvent == None:
        msg = "Tier0Config.addExpressConfig : no timePerEvent defined for stream %s" % streamName
        raise RuntimeError(msg)
    streamConfig.Express.TimePerEvent = timePerEvent

    sizePerEvent = options.get("sizePerEvent", None)
    if sizePerEvent == None:
        msg = "Tier0Config.addExpressConfig : no sizePerEvent defined for stream %s" % streamName
        raise RuntimeError(msg)
    streamConfig.Express.SizePerEvent = sizePerEvent

    streamConfig.Express.MaxInputRate = options.get("maxInputRate", 23 * 1000)
    streamConfig.Express.MaxInputEvents = options.get("maxInputEvents", 200)
    streamConfig.Express.MaxInputSize = options.get("maxInputSize", 2 * 1024 * 1024 * 1024)
    streamConfig.Express.MaxInputFiles = options.get("maxInputFiles", 500)
    streamConfig.Express.MaxLatency = options.get("maxLatency", 15 * 23)

    streamConfig.Express.PeriodicHarvestInterval = options.get("periodicHarvestInterval", 0)

    streamConfig.Express.DataType = options.get("dataType", "express")

    streamConfig.Express.ArchivalNode = options.get("archivalNode", None)
    streamConfig.Express.TapeNode = options.get("tapeNode", None)
    streamConfig.Express.DiskNode = options.get("diskNode", None)
    streamConfig.Express.PhEDExGroup = options.get("phedexGroup", "express")

    streamConfig.Express.BlockCloseDelay = options.get("blockCloseDelay", 3600)

    if hasattr(streamConfig.Express, "MaxMemoryperCore"):
        streamConfig.Express.MaxMemoryperCore = options.get("maxMemoryperCore", streamConfig.Express.MaxMemoryperCore)
    else:
        streamConfig.Express.MaxMemoryperCore = options.get("maxMemoryperCore", 2000)

    if hasattr(streamConfig, "datasetLifetime"):
        streamConfig.Express.datasetLifetime = options.get("dataset_lifetime", streamConfig.Express.datasetLifetime)
    else:
        streamConfig.Express.datasetLifetime = options.get("dataset_lifetime", 0)

    return

def addSiteConfig(config, siteName, **options):
    """
    _addSiteConfig_
    Add a site configuration.
    """
    siteConfig = retrieveSiteConfig(config, siteName)

    if hasattr(siteConfig, "OverrideCatalog"):
        siteConfig.OverrideCatalog = options.get("overrideCatalog", siteConfig.OverrideCatalog)
    else:
        siteConfig.OverrideCatalog = options.get("overrideCatalog", "trivialcatalog_file:/cvmfs/cms.cern.ch/local/T0_CH_CERN/PhEDEx/storage.xml?protocol=eos")

    if hasattr(siteConfig, "SiteLocalConfig"):
        siteConfig.SiteLocalConfig = options.get("siteLocalConfig", siteConfig.SiteLocalConfig)
    else:
        siteConfig.SiteLocalConfig = options.get("siteLocalConfig", "/cvmfs/cms.cern.ch/SITECONF/local/JobConfig/site-local-config.xml")

    return

def addRegistrationConfig(config, streamName, **options):
    """
    _addRegistrationConfig_

    Add an registration configuration to a given stream.

    Sets the streams processing style to either 'Register' or
    'RegisterAndConvert', depending on whether there is
    also a addConversionConfig call
    """
    primds = options.get("primds", None)
    if primds == None:
        msg = "Tier0Config.addRegistrationConfig : no primary dataset defined for stream %s" % streamName
        raise RuntimeError(msg)

    data_tier = options.get("data_tier", None)
    if data_tier == None:
        msg = "Tier0Config.addRegistrationConfig : no data_tier defined for stream %s" % streamName
        raise RuntimeError(msg)

    acq_era = options.get("acq_era", None)
    if acq_era == None:
        msg = "Tier0Config.addRegistrationConfig : no acquisition era defined for stream %s" % streamName
        raise RuntimeError(msg)

    proc_version = options.get("proc_version", None)
    if proc_version == None:
        msg = "Tier0Config.addRegistrationConfig : no processing version defined for stream %s" % streamName
        raise RuntimeError(msg)

    proc_string = options.get("proc_string", None)

    streamConfig = retrieveStreamConfig(config, streamName)
    if streamConfig.ProcessingStyle == "Convert" or \
       streamConfig.ProcessingStyle == "RegisterAndConvert":
        streamConfig.ProcessingStyle = "RegisterAndConvert"
    else:
        streamConfig.ProcessingStyle = "Register"
    streamConfig.VersionOverride = options.get("versionOverride", {})

    streamConfig.section_("Register")

    streamConfig.Register.PrimaryDataset = primds
    streamConfig.Register.DataTier = data_tier

    if proc_string == None:
        streamConfig.Register.ProcessedDataset = "%s-%s" % (acq_era, proc_version)
    else:
        streamConfig.Register.ProcessedDataset = "%s-%s-%s" % (acq_era, proc_string, proc_version)

    return

def addConversionConfig(config, streamName, **options):
    """
    _addConversionConfig_

    Add an conversion configuration to a given stream.

    Sets the streams processing style to either 'Convert' or
    'RegisterAndConvert', depending on whether there is
    also a addRegistrationConfig call
    """
    primds = options.get("primds", None)
    if primds == None:
        msg = "Tier0Config.addConversionConfig : no primary dataset defined for stream %s" % streamName
        raise RuntimeError(msg)

    data_tier = options.get("data_tier", None)
    if data_tier == None:
        msg = "Tier0Config.addConversionConfig : no data tier defined for stream %s" % streamName
        raise RuntimeError(msg)

    conv_type = options.get("conv_type", None)
    if conv_type == None:
        msg = "Tier0Config.addConversionConfig : no conversion type defined for stream %s" % streamName
        raise RuntimeError(msg)

    acq_era = options.get("acq_era", None)
    if acq_era == None:
        msg = "Tier0Config.addConversionConfig : no acquisition era defined for stream %s" % streamName
        raise RuntimeError(msg)

    proc_version = options.get("proc_version", None)
    if proc_version == None:
        msg = "Tier0Config.addConversionConfig : no processing version defined for stream %s" % streamName
        raise RuntimeError(msg)

    proc_string = options.get("proc_string", None)

    streamConfig = retrieveStreamConfig(config, streamName)
    if streamConfig.ProcessingStyle == "Register" or \
       streamConfig.ProcessingStyle == "RegisterAndConvert":
        streamConfig.ProcessingStyle = "RegisterAndConvert"
    else:
        streamConfig.ProcessingStyle = "Convert"
    streamConfig.VersionOverride = options.get("versionOverride", {})

    streamConfig.section_("Convert")

    streamConfig.Convert.PrimaryDataset = primds
    streamConfig.Convert.DataTier = data_tier
    streamConfig.Convert.Type = conv_type

    streamConfig.Convert.AcqEra = acq_era
    streamConfig.Convert.ProcVers = proc_version
    streamConfig.Convert.ProcString = proc_string
    
    if proc_string == None:
        streamConfig.Convert.ProcessedDataset = "%s-%s" % (acq_era, proc_version)
    else:
        streamConfig.Convert.ProcessedDataset = "%s-%s-%s" % (acq_era, proc_string, proc_version)

    return

def addTier1Skim(config, skimName, dataTier, primaryDataset, cmsswVersion,
                 processingVersion, configURL, globalTag, twoFileRead = False,
                 skimNode = None):
    """
    _addTier1Skim_

    Add the configuration of a skim that is to be run over a particular primary
    dataset and data tier at a particular site to the Tier0 configuration.  The
    skims will be launched as blocks are transfered to the site.  The site name
    must correspond to the site name in the ProdAgent JobQueue.
    """
    datasetConfig = config.Datasets.section_(primaryDataset)    

    skimConfig = ConfigSection(name = "SomeTier1Skim")
    skimConfig.PrimaryDataset = primaryDataset
    skimConfig.DataTier = dataTier
    skimConfig.SkimName = skimName
    skimConfig.CMSSWVersion = cmsswVersion
    skimConfig.ConfigURL = configURL
    skimConfig.GlobalTag = globalTag
    skimConfig.ProcessingVersion = processingVersion
    skimConfig.TwoFileRead = twoFileRead
    skimConfig.Node = skimNode

    datasetConfig.Tier1Skims.append(skimConfig)
    return
