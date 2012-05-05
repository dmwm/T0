"""
_Tier0Config_

Utility methods for creating and manipulating a Tier0 configuration

The Tier0 configuration has the following form:

Tier0Configuration - Global configuration object
| | |
| | |--> Global - Configuration parameters that do not belong to a particular
| |       |       stream or dataset and can be applied to an entire run.
| |       |
| |       |--> Version - The CVS revision of the config
| |       |--> AcquisitionEra - The acquisition era for the run
| |       |--> RecoTimeout - PromptReco release timeout
| |       |--> RecoLockTimeout - timout for locking PromptReco release before
| |       |                      actual release
| |       |--> PhEDExSubscriptions - Dictionary of PhEDEx subscriptions where the
| |                                  primary dataset id is the key and the storage
| |                                  node name is the value
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
|             |     |--> Nothing here for now, placeholder
|             |
|             |--> Express - Configuration section for express streams
|             |     |
|             |     |--> Scenario - Event scenario, determines configurations used
|             |     |
|             |     |--> ProcessingConfigURL - URL to the processing configuration
|             |     |
|             |     |--> DataTiers - List of data tiers
|             |     |
|             |     |--> AlcaMergeConfigURL - URL to the Alca merge configuration
|             |     |
|             |     |--> GlobalTag - Global tag used for processing
|             |     |
|             |     |--> Producers - List of alca producers active for this stream.
|             |     |
|             |     |--> ProcessingVersion - processing version
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
            |--> Scenario - String that describes the processing scenario for this
            |               dataset.
            |--> CustodialNode - The custodial PhEDEx storage node for this dataset
            |--> ArchivalNode - The archival PhEDEx node, always CERN.
            |--> CustodialPriority - The priority of the custodial subscription
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
            |     |--> GlobalTag - The global tag that will be used to prompt
            |     |                reconstruction.  Only used if DoReco is true.
            |     |--> CMSSWVersion - Framework version to be used for prompt
            |     |                   reconstruction.  This only needs to be filled
            |     |                   in if DoReco is True and will default to 
            |     |                   Undefined if not set.
            |     |--> ConfigURL - URL of the framework configuration file.  If not set
            |                      the configuration will be pulled from the framework.
            |
            |--> Alca - Configuration section to hold settings related to alca 
            |     |     production.
            |     |
            |     |--> DoAlca - Either True or False.  Determines whether alca production
            |     |             is preformed on this dataset.
            |     |--> ConfigURL - URL of the framework configuration file.  If not set 
            |                      the configuration will be pulled from the framework.
            |
            |--> Tier1Skims - List of configuration section objects to hold Tier1 skims for
                  |           this dataset.
                  |
                  |--> DataTier - The tier of the input data.
                  |--> PrimaryDataset - The primary dataset of the input data.
                  |--> GlobalTag - The global tag to use with the skim.
                  |--> CMSSWVersion - The framework version to use with the skim.
                  |--> SkimName - The name of the skim.  Used for generating more descriptive job names.
                  |--> ConfigURL - A URL to the framework config for the config.
                  |--> ProcessingVersion - The processing version of the skim.
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

    # setup some defaults
    tier0Config.Global.RecoTimeout = 0
    tier0Config.Global.RecoLockTimeout = 0

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
    datasetConfig.Reco.ConfigURL = settings.get("reco_configuration", None)
    datasetConfig.Reco.ProcessingVersion = settings.get("reco_proc_ver", datasetConfig.ProcessingVersion)
    datasetConfig.Reco.EventSplit = settings.get("reco_split", 2000)
    datasetConfig.Reco.WriteRECO = settings.get("write_reco", True)
    datasetConfig.Reco.WriteDQM = settings.get("write_dqm", True)
    datasetConfig.Reco.WriteAOD = settings.get("write_aod", True)

    datasetConfig.Alca.DoAlca = settings.get("do_alca", False)
    datasetConfig.Alca.Producers = settings.get("alca_producers", [])
    datasetConfig.Alca.ConfigURL = settings.get("alca_configuration", None)

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

def setRecoTimeout(config, recoTimeout):
    """
    _setRecoTimeout__

    Set the reco timeout in the configuration.
    """
    config.Global.RecoTimeout = recoTimeout
    return

def setRecoLockTimeout(config, recoLockTimeout):
    """
    _setRecoLockTimeout_

    Set the reco lock timeout in the configuration.
    """
    config.Global.RecoLockTimeout = recoLockTimeout
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
    streamConfig.Express.ProcessingConfigURL = proc_config
    streamConfig.Express.DataTiers = data_tiers
    streamConfig.Express.AlcaMergeConfigURL = alcamerge_config
    streamConfig.Express.GlobalTag = global_tag

    streamConfig.Express.Producers = options.get("alca_producers", [])
    streamConfig.Express.ProcessingVersion = options.get("proc_ver", 1)
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
