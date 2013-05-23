"""
_Tier0Config_

Utility methods for creating and manipulating a Tier0 configuration

The Tier0 configuration has the following form:

Tier0Configuration - Global configuration object
| | |
| | |--> Global - Configuration parameters that do not belong to a particular
| |       |       stream or dataset and can be applied to an entire run.
| |       |
| |       |--> Version - The configuration version (not used at the moment)
| |       |
| |       |--> AcquisitionEra - The acquisition era for the run
| |       |
| |       |--> LFNPrefix - The LFN prefix for the run
| |       |
| |       |--> BulkDataType - The bulk data type for the run
| |       |
| |       |--> BulkDataLocation - The bulk data location for the run (to be used as phedex source site)
| |       |
| |       |--> DQMUploadURL - The URL used for DQM uploads
| |       |
| |       |--> AlcaHarvestTimeout - AlcaHarvesting for a run/stream is normally trigered by
| |       |                         fileset closing (ie. all data received and processed).
| |       |                         This timeout will configure an additional time trigger
| |       |                         based on the run end_time (or when the last streamer
| |       |                         file was received).
| |       |
| |       |--> AlcaHarvestDir - Directory to which the AlcaHarvest job copies the
| |       |                     sqlite file and associated metadata.
| |       |
| |       |--> ConditionUploadTimeout - ConditionUpload normally only advances to the next run
| |       |                             if the current run is completely finished (ie. all data
| |       |                             received, processed, alca harvested and conditions
| |       |                             uploaded). This timeout will configure an additional
| |       |                             time trigger based on the run end_time ( or when the
| |       |                             last streamer file was received).
| |       |
| |       |--> DropBoxHost - Machine where we upload the PCL conditions to
| |       |
| |       |--> ValidationMode - Whether or not we upload conditions for immediate use
| |                             in PromptReco or just for validation checks.
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
|             |
|             |--> Express - Configuration section for express streams
|             |     |
|             |     |--> Scenario - Event scenario, determines configurations used
|             |     |
|             |     |--> DataTiers - List of data tiers
|             |     |
|             |     |--> GlobalTag - Global tag used for processing
|             |     |
|             |     |--> AlcaSkims - List of alca skims active for this stream.
|             |     |
|             |     |--> DqmSequences - List of dqm sequences active for this stream.
|             |     |
|             |     |--> ProcessingVersion - processing version
|             |     |
|             |     |--> MaxInputEvents - max input events for express processing job
|             |     |
|             |     |--> MaxInputSize - max input size for express merge job
|             |     |
|             |     |--> MaxInputFiles - max input files for express merge job
|             |     |
|             |     |--> MaxLatency - max latency to trigger express merge job
|             |     |
|             |     |--> BlockCloseDelay - delay to close block in WMAgent
|             |
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
      | |--> Default - Configuration section to hold the default dataset config.
      |                This will have the same structure as the dataset config
      |                listed below.
      |
      |--> DATASETNAME
            |--> Name - Name of the dataset.
            |
            |--> Scenario - Processing scenario for this dataset.
            |
            |--> RecoDelay - PromptReco delay
            |
            |--> RecoDelayOffset - Time before PromptReco release for which
            |                      settings are locked in and reco looks released
            |
            |--> CustodialNode - The custodial PhEDEx storage node for this dataset
            |
            |--> ArchivalNode - The archival PhEDEx node, always CERN.
            |
            |--> CustodialPriority - The priority of the custodial subscription
            |
            |--> CustodialAutoApprove - Determine whether or not the custodial
            |                           subscription will be auto approved.
            |
            |--> DefaultProcessingVersion - Used for all output from PromptReco
            |
            |--> Reco - Configuration section to hold settings related to prompt
            |     |     reconstruction.
            |     |
            |     |--> DoReco - Either True or False.  Determines whether prompt
            |     |             reconstruction is preformed on this dataset.
            |     |
            |     |--> GlobalTag - The global tag that will be used to prompt
            |     |                reconstruction.  Only used if DoReco is true.
            |     |
            |     |--> CMSSWVersion - Framework version to be used for prompt
            |     |                   reconstruction.  This only needs to be filled
            |     |                   in if DoReco is True and will default to
            |     |                   Undefined if not set.
            |     |
            |     |--> AlcaSkims - List of alca skims active for this dataset.
            |     |
            |     |--> DqmSequences - List of dqm sequences active for this dataset.
            |
            |--> Tier1Skims - List of configuration section objects to hold Tier1 skims for
                  |           this dataset.
                  |
                  |--> DataTier - The tier of the input data.
                  |
                  |--> PrimaryDataset - The primary dataset of the input data.
                  |
                  |--> GlobalTag - The global tag to use with the skim.
                  |
                  |--> CMSSWVersion - The framework version to use with the skim.
                  |
                  |--> SkimName - The name of the skim.  Used for generating more descriptive job names.
                  |
                  |--> ConfigURL - A URL to the framework config for the config.
                  |
                  |--> ProcessingVersion - The processing version of the skim.
                  |
                  |--> TwoFileRead - Bool that determines if this is a two file read skim.
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
    tier0Config.section_("Global")

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

def retrieveDatasetConfig(config, datasetName):
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

    return datasetConfig


def addDataset(config, datasetName, **settings):
    """
    _addDataset_

    Add a dataset to the configuration using settings from the Default dataset
    to fill in any parameter not explicitly defined here. Default is doing nothing.

    The following keys may be passed in to alter the default settings:
      scenario - The scenario for this dataset.
      global_tag - The global tag to use for reco.
      do_reco, do_alca - Disable/enable reco and alca.
        Default is disabled for both.
      reco_version - Framework versions for reco and alca.
        No defaults are specified.
      default_proc_ver - Processing version that will be applied to all
        processing steps.  This will be applied first and then the specific
        processing versions will be applied.
      reco_configuration, alca_configuration - Configurations
        to use for reco and alca.  No defaults are specified.
      alca_producers - The list of alca producers to be run during reco and
        which we need to then split out during alca skimming
      reco_split - The amount of events to process per prompt reco job  
      custodial_node - The PhEDEx custodial node for this dataset.
      archival_node - The PhEDEx archival node for this dataset, always CERN.
      custodial_priority - The priority of the custodial PhEDEx subscription,
        defaults to high.
      custodial_auto_approve - Whether or not the custodial subscription is auto
        approved.  Defaults to false.
    """
    datasetConfig = retrieveDatasetConfig(config, datasetName)

    # scenario needs to be specified
    if hasattr(datasetConfig, "Scenario"):
        datasetConfig.Scenario = settings.get('scenario', datasetConfig.Scenario)
        if datasetConfig.Scenario == None:
            msg = "Tier0Config.addDataset : no scenario defined for dataset %s or in Default" % datasetName
            raise RuntimeError, msg
    else:
        datasetConfig.Scenario = settings.get('scenario', None)

    datasetConfig.section_("Reco")
    datasetConfig.section_("Alca")

    #
    # override default settings with dataset specific settings (if exists)
    #
    if hasattr(datasetConfig, "RecoDelay"):
        datasetConfig.RecoDelay = settings.get('reco_delay', datasetConfig.RecoDelay)
    else:
        datasetConfig.RecoDelay = settings.get('reco_delay', 48 * 3600)

    if hasattr(datasetConfig, "RecoDelayOffset"):
        datasetConfig.RecoDelayOffset = settings.get('reco_delay_offset', datasetConfig.RecoDelayOffset)
    else:
        datasetConfig.RecoDelayOffset = settings.get('reco_delay_offset', 30 * 60)

    if datasetConfig.RecoDelayOffset > datasetConfig.RecoDelay:
        datasetConfig.RecoDelayOffset = datasetConfig.RecoDelay

    if hasattr(datasetConfig, "ProcessingVersion"):
        datasetConfig.ProcessingVersion = settings.get('default_proc_ver', datasetConfig.ProcessingVersion)
    else:
        datasetConfig.ProcessingVersion = settings.get('default_proc_ver', None)

    if hasattr(datasetConfig, "GlobalTag"):
        datasetConfig.GlobalTag = settings.get('global_tag', datasetConfig.GlobalTag)
    else:
        datasetConfig.GlobalTag = settings.get('global_tag', None)

    if hasattr(datasetConfig, "ArchivalNode"):
        datasetConfig.ArchivalNode = settings.get('archival_node', datasetConfig.ArchivalNode)
    else:
        datasetConfig.ArchivalNode = settings.get('archival_node', None)

    if hasattr(datasetConfig.Reco, "CMSSWVersion"):
        datasetConfig.Reco.CMSSWVersion = settings.get('reco_version', datasetConfig.Reco.CMSSWVersion)
    else:
        datasetConfig.Reco.CMSSWVersion = settings.get('reco_version', "Undefined")

    datasetConfig.Reco.DoReco = settings.get("do_reco", False)
    datasetConfig.Reco.GlobalTag = settings.get("global_tag", datasetConfig.GlobalTag)
    datasetConfig.Reco.ProcessingVersion = settings.get("reco_proc_ver", datasetConfig.ProcessingVersion)
    datasetConfig.Reco.EventSplit = settings.get("reco_split", 2000)
    datasetConfig.Reco.WriteRECO = settings.get("write_reco", True)
    datasetConfig.Reco.WriteDQM = settings.get("write_dqm", True)
    datasetConfig.Reco.WriteAOD = settings.get("write_aod", True)
    datasetConfig.Reco.AlcaSkims = settings.get("alca_producers", [])
    datasetConfig.Reco.DqmSequences = settings.get("dqm_sequences", [])

    datasetConfig.CustodialNode = settings.get("custodial_node", None)
    datasetConfig.CustodialPriority = settings.get("custodial_priority", "high")
    datasetConfig.CustodialAutoApprove = settings.get("custodial_auto_approve", False)

    datasetConfig.Tier1Skims = []
    return

def setAcquisitionEra(config, acquisitionEra):
    """
    _setAcquisitionEra_

    Set the acquisition era in the configuration.
    """
    config.Global.AcquisitionEra = acquisitionEra
    return

def setLFNPrefix(config, prefix):
    """
    _setLFNPrefix_

    Set the LFN prefix in the configuration.
    """
    config.Global.LFNPrefix = prefix
    return

def setBulkDataType(config, type):
    """
    _setBulkDataType_

    Set the bulk data type in the configuration.
    """
    config.Global.BulkDataType = type
    return

def setBulkDataLocation(config, location):
    """
    _setBulkDataLocation_

    Set the bulk data location (to be used as source for phedex injections) in the configuration.
    
    """
    config.Global.BulkDataLocation = location
    return

def setDQMUploadUrl(config, dqmuploadurl):
    """
    _setDQMUploadUrl_

    Set the DQM upload Url in the configuration.
    
    """
    config.Global.DQMUploadUrl = dqmuploadurl
    return

def setPromptCalibrationConfig(config, alcaHarvestTimeout, alcaHarvestDir,
                               conditionUploadTimeout, dropboxHost,
                               validationMode):
    """
    _setPromptCalibrationConfig_

    Configure needed settings for PromptCalibration
    """
    config.Global.AlcaHarvestTimeout = alcaHarvestTimeout
    config.Global.AlcaHarvestDir = alcaHarvestDir
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

    if streamConfig.Repack.MaxOverSize > streamConfig.Repack.MaxEdmSize:
        streamConfig.Repack.MaxOverSize = streamConfig.Repack.MaxEdmSize

    return

def addExpressConfig(config, streamName, **options):
    """
    _addExpressConfig_

    Add an express configuration to a given stream.

    """
    scenario = options.get("scenario", None)
    if scenario == None:
        msg = "Tier0Config.addExpressConfig : no scenario defined for stream %s" % streamName
        raise RuntimeError, msg

    proc_config = options.get("proc_config", None)

    data_tiers = options.get("data_tiers", [])
    if type(data_tiers) != list or len(data_tiers) == 0:
        msg = "Tier0Config.addExpressConfig : data_tiers needs to be list with at least one tier"
        raise RuntimeError, msg

    alcamerge_config = None
    if "ALCARECO" in data_tiers:
        alcamerge_config = options.get("alcamerge_config", None)

    global_tag = options.get("global_tag", None)

    streamConfig = retrieveStreamConfig(config, streamName)
    streamConfig.ProcessingStyle = "Express"
    streamConfig.VersionOverride = options.get("versionOverride", {})

    streamConfig.section_("Express")

    streamConfig.Express.Scenario = scenario
    streamConfig.Express.DataTiers = data_tiers
    streamConfig.Express.GlobalTag = global_tag

    streamConfig.Express.AlcaSkims = options.get("alca_producers", [])
    streamConfig.Express.DqmSequences = options.get("dqm_sequences", [])
    streamConfig.Express.ProcessingVersion = options.get("proc_ver", 1)

    streamConfig.Express.MaxInputEvents = options.get("maxInputEvents", 200)
    streamConfig.Express.MaxInputSize = options.get("maxInputSize", 2 * 1024 * 1024 * 1024)
    streamConfig.Express.MaxInputFiles = options.get("maxInputFiles", 500)
    streamConfig.Express.MaxLatency = options.get("maxLatency", 15 * 23)

    streamConfig.Express.BlockCloseDelay = options.get("blockCloseDelay", 3600)

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
        raise RuntimeError, msg

    data_tier = options.get("data_tier", None)
    if data_tier == None:
        msg = "Tier0Config.addRegistrationConfig : no data_tier defined for stream %s" % streamName
        raise RuntimeError, msg

    acq_era = options.get("acq_era", None)
    if acq_era == None:
        msg = "Tier0Config.addRegistrationConfig : no acquisition era defined for stream %s" % streamName
        raise RuntimeError, msg

    proc_version = options.get("proc_version", None)
    if proc_version == None:
        msg = "Tier0Config.addRegistrationConfig : no processing version defined for stream %s" % streamName
        raise RuntimeError, msg

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
        raise RuntimeError, msg

    data_tier = options.get("data_tier", None)
    if data_tier == None:
        msg = "Tier0Config.addConversionConfig : no data tier defined for stream %s" % streamName
        raise RuntimeError, msg

    conv_type = options.get("conv_type", None)
    if conv_type == None:
        msg = "Tier0Config.addConversionConfig : no conversion type defined for stream %s" % streamName
        raise RuntimeError, msg

    acq_era = options.get("acq_era", None)
    if acq_era == None:
        msg = "Tier0Config.addConversionConfig : no acquisition era defined for stream %s" % streamName
        raise RuntimeError, msg

    proc_version = options.get("proc_version", None)
    if proc_version == None:
        msg = "Tier0Config.addConversionConfig : no processing version defined for stream %s" % streamName
        raise RuntimeError, msg

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
