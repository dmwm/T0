"""
_OfflineConfiguration_

Processing configuration for the Tier0 - Production version for HI
"""
from __future__ import print_function

from T0.RunConfig.Tier0Config import addDataset
from T0.RunConfig.Tier0Config import createTier0Config
from T0.RunConfig.Tier0Config import setAcquisitionEra
from T0.RunConfig.Tier0Config import setScramArch
from T0.RunConfig.Tier0Config import setDefaultScramArch
from T0.RunConfig.Tier0Config import setBaseRequestPriority
from T0.RunConfig.Tier0Config import setBackfill
from T0.RunConfig.Tier0Config import setBulkDataType
from T0.RunConfig.Tier0Config import setProcessingSite
from T0.RunConfig.Tier0Config import setExpressSubscribeNode
from T0.RunConfig.Tier0Config import setDQMDataTier
from T0.RunConfig.Tier0Config import setDQMUploadUrl
from T0.RunConfig.Tier0Config import setPromptCalibrationConfig
from T0.RunConfig.Tier0Config import setConfigVersion
from T0.RunConfig.Tier0Config import ignoreStream
from T0.RunConfig.Tier0Config import addRepackConfig
from T0.RunConfig.Tier0Config import addExpressConfig
from T0.RunConfig.Tier0Config import addRegistrationConfig
from T0.RunConfig.Tier0Config import addConversionConfig

# Create the Tier0 configuration object
tier0Config = createTier0Config()

# Set the verstion configuration (not used at the moment)
setConfigVersion(tier0Config, "replace with real version")

# Settings up sites
processingSite = "T0_CH_CERN"

# Set global parameters:
#  Acquisition era
#  BaseRequestPriority
#  Backfill mode
#  Data type
#  Processing site (where jobs run)
#  PhEDEx locations
setAcquisitionEra(tier0Config, "PARun2016C")
setBaseRequestPriority(tier0Config, 250000)
setBackfill(tier0Config, None)
setBulkDataType(tier0Config, "hidata")
setProcessingSite(tier0Config, processingSite)
setExpressSubscribeNode(tier0Config, "T2_CH_CERN")

# Override for DQM data tier
setDQMDataTier(tier0Config, "DQMIO")

# Define the two default timeouts for reco release
# First timeout is used directly for reco release
# Second timeout is used for the data service PromptReco start check
# (to basically say we started PromptReco even though we haven't)
defaultRecoTimeout =  48 * 3600
defaultRecoLockTimeout = 1800

# DQM Server
setDQMUploadUrl(tier0Config, "https://cmsweb.cern.ch/dqm/offline")

# PCL parameters
setPromptCalibrationConfig(tier0Config,
                           alcaHarvestTimeout = 12*3600,
                           alcaHarvestDir = "/store/express/tier0_harvest",
                           conditionUploadTimeout = 18*3600,
                           dropboxHost = "webcondvm.cern.ch",
                           validationMode = False)

# Special syntax supported for cmssw version, processing version and global tag
#
# { 'acqEra': {'Era1': Value1, 'Era2': Value2},
#   'maxRun': {100000: Value3, 200000: Value4},
#   'default': Value5 }

# Defaults for CMSSW version
defaultCMSSWVersion = "CMSSW_8_0_24"

# Configure ScramArch
setDefaultScramArch(tier0Config, "slc6_amd64_gcc530")

# Configure scenarios
ppScenario = "ppEra_Run2_2016"
ppScenarioB0T = "ppEra_Run2_2016"
cosmicsScenario = "cosmicsEra_Run2_2016"
hcalnzsScenario = "hcalnzsEra_Run2_2016"
hiScenario = "ppEra_Run2_2016_pA"

# Defaults for processing version
defaultProcVersionRAW = 1

defaultProcVersionReco = {
       'acqEra': {'Run2016H': "3"},
       'default': "1"
     }

expressProcVersion = {
       'acqEra': {'Run2016H': "3"},
       'default': "1"
     }

alcarawProcVersion = {
       'acqEra': {'Run2016H': "2"},
       'default': "1"
     }

# Defaults for GlobalTag
expressGlobalTag = "80X_dataRun2_Express_v15"
promptrecoGlobalTag = "80X_dataRun2_Prompt_v15"
alcap0GlobalTag = "80X_dataRun2_Prompt_v15"

# Mandatory for CondDBv2
globalTagConnect = "frontier://PromptProd/CMS_CONDITIONS"

# Multicore settings
numberOfCores = 4

# Splitting parameters for PromptReco
defaultRecoSplitting = 10000 * numberOfCores
hiRecoSplitting = 200 * numberOfCores
alcarawSplitting = 20000 * numberOfCores

#
# Setup repack and express mappings
#
repackVersionOverride = {
    }

expressVersionOverride = {
    "CMSSW_8_0_0" : "CMSSW_8_0_24",
    "CMSSW_8_0_1" : "CMSSW_8_0_24",
    "CMSSW_8_0_2" : "CMSSW_8_0_24",
    "CMSSW_8_0_3" : "CMSSW_8_0_24",
    "CMSSW_8_0_4" : "CMSSW_8_0_24",
    "CMSSW_8_0_5" : "CMSSW_8_0_24",
    "CMSSW_8_0_6" : "CMSSW_8_0_24",
    "CMSSW_8_0_7" : "CMSSW_8_0_24",
    "CMSSW_8_0_8" : "CMSSW_8_0_24",
    "CMSSW_8_0_9" : "CMSSW_8_0_24",
    "CMSSW_8_0_10" : "CMSSW_8_0_24",
    "CMSSW_8_0_11" : "CMSSW_8_0_24",
    "CMSSW_8_0_12" : "CMSSW_8_0_24",
    "CMSSW_8_0_13" : "CMSSW_8_0_24",
    "CMSSW_8_0_14" : "CMSSW_8_0_24",
    "CMSSW_8_0_15" : "CMSSW_8_0_24",
    "CMSSW_8_0_16" : "CMSSW_8_0_24",
    "CMSSW_8_0_17" : "CMSSW_8_0_24",
    "CMSSW_8_0_18" : "CMSSW_8_0_24",
    "CMSSW_8_0_19" : "CMSSW_8_0_24",
    "CMSSW_8_0_20" : "CMSSW_8_0_24",
    "CMSSW_8_0_21" : "CMSSW_8_0_24",
    "CMSSW_8_0_22" : "CMSSW_8_0_24",
    "CMSSW_8_0_23" : "CMSSW_8_0_24"
    }

#set default repack settings for bulk streams
addRepackConfig(tier0Config, "Default",
                proc_ver = defaultProcVersionRAW,
                maxSizeSingleLumi = 12 * 1024 * 1024 * 1024,
                maxSizeMultiLumi = 8 * 1024 * 1024 * 1024,
                minInputSize =  2.1 * 1024 * 1024 * 1024,
                maxInputSize = 4 * 1024 * 1024 * 1024,
                maxEdmSize = 12 * 1024 * 1024 * 1024,
                maxOverSize = 8 * 1024 * 1024 * 1024,
                maxInputEvents = 3 * 1000 * 1000,
                maxInputFiles = 1000,
                maxLatency = 24 * 3600,
                blockCloseDelay = 24 * 3600,
                versionOverride = repackVersionOverride)

addDataset(tier0Config, "Default",
           do_reco = False,
           write_reco = False, write_aod = True, write_miniaod = False, write_dqm = False,
           reco_delay = defaultRecoTimeout,
           reco_delay_offset = defaultRecoLockTimeout,
           reco_split = defaultRecoSplitting,
           proc_version = defaultProcVersionReco,
           cmssw_version = defaultCMSSWVersion,
           multicore = numberOfCores,
           global_tag = promptrecoGlobalTag,
           global_tag_connect = globalTagConnect,
           archival_node = "T0_CH_CERN_MSS",
           tape_node = "T1_US_FNAL_MSS",
           disk_node = "T1_US_FNAL_Disk",
           raw_to_disk = False,
           blockCloseDelay = 24 * 3600,
           timePerEvent = 5,
           sizePerEvent = 1500,
           scenario = ppScenario)

###############################
### PDs used during Run2015 ###
###############################

addDataset(tier0Config, "Cosmics",
           do_reco = True,
           write_reco = True,
           write_miniaod = False, write_dqm = True,
           alca_producers = [ "TkAlCosmics0T", "MuAlGlobalCosmics", "HcalCalHOCosmics", "DtCalibCosmics" ],
           physics_skims = [ "CosmicSP", "CosmicTP", "LogError", "LogErrorMonitor" ],
           timePerEvent = 0.5,
           sizePerEvent = 155,
           scenario = cosmicsScenario)

addDataset(tier0Config, "Commissioning",
           do_reco = True,
           raw_to_disk = True,
           write_dqm = True,
           alca_producers = [ "TkAlMinBias", "SiStripCalMinBias", "HcalCalIsoTrk", "HcalCalIsolatedBunchSelector" ],
           dqm_sequences = [ "@common", "@hcal" ],
           physics_skims = [ "EcalActivity", "LogError", "LogErrorMonitor" ],
           timePerEvent = 12,
           sizePerEvent = 4000,
           scenario = ppScenario)

addDataset(tier0Config, "Commissioning_0T",
           do_reco = True,
           raw_to_disk = True,
           write_dqm = True,
           alca_producers = [ "TkAlMinBias", "SiStripCalMinBias", "HcalCalIsoTrk", "HcalCalIsolatedBunchSelector" ],
           dqm_sequences = [ "@common", "@hcal" ],
           physics_skims = [ "EcalActivity", "LogError", "LogErrorMonitor" ],
           timePerEvent = 12,
           sizePerEvent = 4000,
           scenario = ppScenarioB0T)

datasets = [ "NoBPTX" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               alca_producers = [ "TkAlCosmicsInCollisions" ],
               dqm_sequences = [ "@common" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "NoBPTX_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               alca_producers = [ "TkAlCosmicsInCollisions" ],
               dqm_sequences = [ "@common" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "Jet", "EGamma" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

datasets = [ "Jet_0T", "EGamma_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenarioB0T)

datasets = [ "MinimumBias" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               alca_producers = [ "SiStripCalZeroBias", "SiStripCalMinBias", "TkAlMinBias" ],
               scenario = ppScenario)

datasets = [ "MinimumBias_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               alca_producers = [ "SiStripCalZeroBias", "SiStripCalMinBias", "TkAlMinBias" ],
               scenario = ppScenarioB0T)

datasets = [ "MinimumBias1", "MinimumBias2", "MinimumBias3", "MinimumBias4",
             "MinimumBias5", "MinimumBias6", "MinimumBias7", "MinimumBias8",
             "MinimumBias9", "MinimumBias10", "MinimumBias11", "MinimumBias12",
             "MinimumBias13", "MinimumBias14", "MinimumBias15", "MinimumBias16",
             "MinimumBias17", "MinimumBias18", "MinimumBias19", "MinimumBias20" ]         

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               alca_producers = [ "SiStripCalZeroBias", "SiStripCalMinBias", "TkAlMinBias" ],
               scenario = ppScenario)

datasets = [ "MinimumBias1_0T", "MinimumBias2_0T", "MinimumBias3_0T", "MinimumBias4_0T",
             "MinimumBias5_0T", "MinimumBias6_0T", "MinimumBias7_0T", "MinimumBias8_0T",
             "MinimumBias9_0T", "MinimumBias10_0T", "MinimumBias11_0T", "MinimumBias12_0T",
             "MinimumBias13_0T", "MinimumBias14_0T", "MinimumBias15_0T", "MinimumBias16_0T",
             "MinimumBias17_0T", "MinimumBias18_0T", "MinimumBias19_0T", "MinimumBias20_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               alca_producers = [ "SiStripCalZeroBias", "SiStripCalMinBias", "TkAlMinBias" ],
               scenario = ppScenarioB0T)

datasets = [ "L1TechBPTXPlusOnly", "L1TechBPTXMinusOnly", "L1TechBPTXQuiet" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

datasets = [ "L1TechBPTXPlusOnly_0T", "L1TechBPTXMinusOnly_0T", "L1TechBPTXQuiet_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenarioB0T)

########################
### special test PDs ###
########################

addDataset(tier0Config, "HcalNZS",
           do_reco = True,
           write_dqm = True,
           write_miniaod = True,
           dqm_sequences = [ "@common", "@hcal" ],
           alca_producers = [ "HcalCalMinBias" ],
           physics_skims = [ "LogError", "LogErrorMonitor" ],
           timePerEvent = 4.2,
           sizePerEvent = 1900,
           scenario = hcalnzsScenario)

addDataset(tier0Config, "HcalNZS_0T",
           do_reco = True,
           write_dqm = True,
           write_miniaod = True,
           dqm_sequences = [ "@common", "@hcal" ],
           alca_producers = [ "HcalCalMinBias" ],
           physics_skims = [ "LogError", "LogErrorMonitor" ],
           timePerEvent = 4.2,
           sizePerEvent = 1900,
           scenario = hcalnzsScenario)

###########################
### special AlcaRaw PDs ###
###########################

addDataset(tier0Config, "AlCaLumiPixels",
           do_reco = True,
           write_reco = False, write_aod = False, write_miniaod = False, write_dqm = True,
           disk_node = None,
           tape_node = None,
           reco_split = alcarawSplitting,
           proc_version = alcarawProcVersion,
           alca_producers = [ "LumiPixels" ],
           dqm_sequences = [ "@common" ],
           timePerEvent = 0.02,
           sizePerEvent = 38,
           scenario = "AlCaLumiPixels")

addDataset(tier0Config, "AlCaLumiPixels0",
           do_reco = True,
           write_reco = False, write_aod = False, write_miniaod = False, write_dqm = True,
           disk_node = None,
           tape_node = None,
           reco_split = alcarawSplitting,
           proc_version = alcarawProcVersion,
           alca_producers = [ "LumiPixels" ],
           dqm_sequences = [ "@common" ],
           timePerEvent = 0.02,
           sizePerEvent = 38,
           scenario = "AlCaLumiPixels")

addDataset(tier0Config, "AlCaLumiPixels1",
           do_reco = True,
           write_reco = False, write_aod = False, write_miniaod = False, write_dqm = True,
           disk_node = None,
           tape_node = None,
           reco_split = alcarawSplitting,
           proc_version = alcarawProcVersion,
           alca_producers = [ "LumiPixels" ],
           dqm_sequences = [ "@common" ],
           timePerEvent = 0.02,
           sizePerEvent = 38,
           scenario = "AlCaLumiPixels")

addDataset(tier0Config, "AlCaLumiPixels2",
           do_reco = True,
           write_reco = False, write_aod = False, write_miniaod = False, write_dqm = True,
           disk_node = None,
           tape_node = None,
           reco_split = alcarawSplitting,
           proc_version = alcarawProcVersion,
           alca_producers = [ "LumiPixels" ],
           dqm_sequences = [ "@common" ],
           timePerEvent = 0.02,
           sizePerEvent = 38,
           scenario = "AlCaLumiPixels")

addDataset(tier0Config, "AlCaLumiPixels3",
           do_reco = True,
           write_reco = False, write_aod = False, write_miniaod = False, write_dqm = True,
           disk_node = None,
           tape_node = None,
           reco_split = alcarawSplitting,
           proc_version = alcarawProcVersion,
           alca_producers = [ "LumiPixels" ],
           dqm_sequences = [ "@common" ],
           timePerEvent = 0.02,
           sizePerEvent = 38,
           scenario = "AlCaLumiPixels")

########################################################
### ZeroBias PDs                                     ###
########################################################

datasets = [ "ZeroBias", "ZeroBias0", "ZeroBias1", "ZeroBias2", 
             "ZeroBias3", "ZeroBias4", "ZeroBias5", "ZeroBias6", 
             "ZeroBias7", "ZeroBias8", "ZeroBias9", "ZeroBias10", 
             "ZeroBias11", "ZeroBias12", "ZeroBias13", "ZeroBias14", 
             "ZeroBias15", "ZeroBias16", "ZeroBias17", "ZeroBias18", 
             "ZeroBias19", "ZeroBias20" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               dqm_sequences = [ "@commonSiStripZeroBias", "@ecal", "@hcal", "@muon" ],
               alca_producers = [ "SiStripCalZeroBias", "TkAlMinBias", "LumiPixelsMinBias" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               timePerEvent = 3.5,
               sizePerEvent = 1500,
               scenario = ppScenario)

datasets = [ "ZeroBias_0T", "ZeroBias0_0T", "ZeroBias1_0T", "ZeroBias2_0T",
             "ZeroBias3_0T", "ZeroBias4_0T", "ZeroBias5_0T", "ZeroBias6_0T", 
             "ZeroBias7_0T", "ZeroBias8_0T", "ZeroBias9_0T", "ZeroBias10_0T", 
             "ZeroBias11_0T", "ZeroBias12_0T", "ZeroBias13_0T", "ZeroBias14_0T", 
             "ZeroBias15_0T", "ZeroBias16_0T", "ZeroBias17_0T", "ZeroBias18_0T", 
             "ZeroBias19_0T", "ZeroBias20_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               dqm_sequences = [ "@commonSiStripZeroBias", "@ecal", "@hcal", "@muon" ],
               alca_producers = [ "SiStripCalZeroBias", "TkAlMinBias", "LumiPixelsMinBias" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               timePerEvent = 3.5,
               sizePerEvent = 1500,
               scenario = ppScenarioB0T)
    
datasets = [ "ZeroBiasFirstBunchAfterTrain", "ZeroBiasFirstBunchInTrain" ]    

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

datasets = [ "ZeroBiasFirstBunchAfterTrain_0T", "ZeroBiasFirstBunchInTrain_0T" ]    

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenarioB0T)

datasets = [ "ZeroBiasIsolatedBunch", "ZeroBiasAfterIsolatedBunch",
             "ZeroBiasIsolatedBunch0", "ZeroBiasIsolatedBunch1", "ZeroBiasIsolatedBunch2",
             "ZeroBiasIsolatedBunch3", "ZeroBiasIsolatedBunch4", "ZeroBiasIsolatedBunch5" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               dqm_sequences = [ "@commonSiStripZeroBias", "@ecal", "@hcal", "@muon" ],
               alca_producers = [ "SiStripCalZeroBias", "TkAlMinBias", "LumiPixelsMinBias" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               timePerEvent = 3.5,
               sizePerEvent = 1500,
               scenario = ppScenario)

datasets = [ "ZeroBiasIsolatedBunch_0T", "ZeroBiasAfterIsolatedBunch_0T",
             "ZeroBiasIsolatedBunch0_0T", "ZeroBiasIsolatedBunch1_0T", "ZeroBiasIsolatedBunch2_0T",
             "ZeroBiasIsolatedBunch3_0T", "ZeroBiasIsolatedBunch4_0T", "ZeroBiasIsolatedBunch5_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               dqm_sequences = [ "@commonSiStripZeroBias", "@ecal", "@hcal", "@muon" ],
               alca_producers = [ "SiStripCalZeroBias", "TkAlMinBias", "LumiPixelsMinBias" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               timePerEvent = 3.5,
               sizePerEvent = 1500,
               scenario = ppScenarioB0T)

datasets = [ "ZeroBiasBunchTrains0", "ZeroBiasBunchTrains1", "ZeroBiasBunchTrains2",
             "ZeroBiasBunchTrains3", "ZeroBiasBunchTrains4", "ZeroBiasBunchTrains5" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               dqm_sequences = [ "@commonSiStripZeroBias", "@ecal", "@hcal", "@muon" ],
               alca_producers = [ "SiStripCalZeroBias", "TkAlMinBias", "LumiPixelsMinBias" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               timePerEvent = 3.5,
               sizePerEvent = 1500,
               scenario = ppScenario)

datasets = [ "ZeroBiasBunchTrains0_0T", "ZeroBiasBunchTrains1_0T", "ZeroBiasBunchTrains2_0T",
             "ZeroBiasBunchTrains3_0T", "ZeroBiasBunchTrains4_0T", "ZeroBiasBunchTrains5_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               dqm_sequences = [ "@commonSiStripZeroBias", "@ecal", "@hcal", "@muon" ],
               alca_producers = [ "SiStripCalZeroBias", "TkAlMinBias", "LumiPixelsMinBias" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               timePerEvent = 3.5,
               sizePerEvent = 1500,
               scenario = ppScenarioB0T)

datasets = [ "ZeroBiasPixelHVScan0", "ZeroBiasPixelHVScan1", "ZeroBiasPixelHVScan2", 
             "ZeroBiasPixelHVScan3", "ZeroBiasPixelHVScan4", "ZeroBiasPixelHVScan5",
             "ZeroBiasPixelHVScan6", "ZeroBiasPixelHVScan7" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               dqm_sequences = [ "@commonSiStripZeroBias", "@ecal", "@hcal", "@muon" ],
               alca_producers = [ "SiStripCalZeroBias", "TkAlMinBias", "LumiPixelsMinBias" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               timePerEvent = 3.5,
               sizePerEvent = 1500,
               scenario = ppScenario)

datasets = [ "ZeroBiasPixelHVScan0_0T", "ZeroBiasPixelHVScan1_0T", "ZeroBiasPixelHVScan2_0T",
             "ZeroBiasPixelHVScan3_0T", "ZeroBiasPixelHVScan4_0T", "ZeroBiasPixelHVScan5_0T",
             "ZeroBiasPixelHVScan6_0T", "ZeroBiasPixelHVScan7_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               dqm_sequences = [ "@commonSiStripZeroBias", "@ecal", "@hcal", "@muon" ],
               alca_producers = [ "SiStripCalZeroBias", "TkAlMinBias", "LumiPixelsMinBias" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               timePerEvent = 3.5,
               sizePerEvent = 1500,
               scenario = ppScenarioB0T)

########################################################
### HLTPhysics PDs                                   ###
########################################################

datasets = [ "HLTPhysics", "HLTPhysicsBunchTrains", "HLTPhysicsIsolatedBunch" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               alca_producers = [ "SiStripCalMinBias", "TkAlMinBias", "HcalCalIsoTrkFilter" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "HLTPhysics_0T", "HLTPhysicsBunchTrains_0T", "HLTPhysicsIsolatedBunch_0T"  ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               alca_producers = [ "SiStripCalMinBias", "TkAlMinBias", "HcalCalIsoTrkFilter" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "HLTPhysics0", "HLTPhysics1", "HLTPhysics2", "HLTPhysics3",
             "HLTPhysics4", "HLTPhysics5", "HLTPhysics6", "HLTPhysics7",
             "HLTPhysics8", "HLTPhysicspart0", "HLTPhysicspart1",
             "HLTPhysicspart2", "HLTPhysicspart3", "HLTPhysicspart4",
             "HLTPhysicspart5", "HLTPhysicspart6", "HLTPhysicspart7"  ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               scenario = ppScenario)

datasets = [ "HLTPhysics0_0T", "HLTPhysics1_0T", "HLTPhysics2_0T", "HLTPhysics3_0T", 
             "HLTPhysics4_0T", "HLTPhysics5_0T", "HLTPhysics6_0T", "HLTPhysics7_0T", 
             "HLTPhysics8_0T", "HLTPhysicspart0_0T", "HLTPhysicspart1_0T",
             "HLTPhysicspart2_0T", "HLTPhysicspart3_0T", "HLTPhysicspart4_0T",
             "HLTPhysicspart5_0T", "HLTPhysicspart6_0T", "HLTPhysicspart7_0T"  ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               scenario = ppScenarioB0T)

################################
### Low PU collisions 13 TeV ###
################################

datasets = [ "CastorJets", "EGMLowPU", "EmptyBX", "FSQJets", "FSQJets1", "FSQJets2", "FSQJets3",
             "FullTrack", "HINCaloJet40", "HINCaloJets", "HINCaloJetsOther", "HINMuon", "HINPFJets",
             "HINPFJetsOther", "HINPhoton", "HighMultiplicity85", "HighMultiplicity85EOF", "L1MinimumBias",
             "L1MinimumBiasHF1", "L1MinimumBiasHF2", "L1MinimumBiasHF3", "L1MinimumBiasHF4",
             "L1MinimumBiasHF5", "L1MinimumBiasHF6", "L1MinimumBiasHF7", "L1MinimumBiasHF8",
             "L1MinimumBias0", "L1MinimumBias1", "L1MinimumBias2", "L1MinimumBias3", "L1MinimumBias4",
             "L1MinimumBias5", "L1MinimumBias6", "L1MinimumBias7", "L1MinimumBias8", "L1MinimumBias9" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

datasets = [ "CastorJets_0T", "EGMLowPU_0T", "EmptyBX_0T", "FSQJets_0T", "FSQJets1_0T", "FSQJets2_0T", "FSQJets3_0T",
             "FullTrack_0T", "HINCaloJet40_0T", "HINCaloJets_0T", "HINCaloJetsOther_0T", "HINMuon_0T",  "HINPFJets_0T",
             "HINPFJetsOther_0T", "HINPhoton_0T", "HighMultiplicity85_0T", "HighMultiplicity85EOF_0T", "L1MinimumBias_0T",
             "L1MinimumBiasHF1_0T", "L1MinimumBiasHF2_0T", "L1MinimumBiasHF3_0T", "L1MinimumBiasHF4_0T",
             "L1MinimumBiasHF5_0T", "L1MinimumBiasHF6_0T", "L1MinimumBiasHF7_0T", "L1MinimumBiasHF8_0T",
             "L1MinimumBias0_0T", "L1MinimumBias1_0T", "L1MinimumBias2_0T", "L1MinimumBias3_0T", "L1MinimumBias4_0T",
             "L1MinimumBias5_0T", "L1MinimumBias6_0T", "L1MinimumBias7_0T", "L1MinimumBias8_0T", "L1MinimumBias9_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenarioB0T)

datasets = [ "HcalHPDNoise" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "HcalHPDNoise_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "HINMuon_HFveto" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

datasets = [ "HINMuon_HFveto_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenarioB0T)

################################
### Special Totem runs       ###
################################

datasets = [ "TOTEM_minBias", "TOTEM_romanPots", "ToTOTEM", "ToTOTEM_DoubleJet32_0", "ToTOTEM_DoubleJet32_1",
             "ToTOTEM_DoubleJet32_2", "ToTOTEM_DoubleJet32_3", "TOTEM_zeroBias", "ZeroBiasTotem", "MinimumBiasTotem",
             "TOTEM_minBias1", "TOTEM_minBias2", "TOTEM_romanPots1", "TOTEM_romanPots2", "TOTEM_romanPots2_0",
             "TOTEM_romanPots2_1", "TOTEM_romanPots2_2", "TOTEM_romanPots2_3", "TOTEM_romanPots2_4",
             "TOTEM_romanPots2_5", "TOTEM_romanPots2_6", "TOTEM_romanPots2_7", "TOTEM_romanPots3",
             "TOTEM_romanPotsTTBB_0", "TOTEM_romanPotsTTBB_1", "TOTEM_romanPotsTTBB_2", "TOTEM_romanPotsTTBB_3",
             "TOTEM_romanPotsTTBB_4", "TOTEM_romanPotsTTBB_5", "TOTEM_romanPotsTTBB_6", "TOTEM_romanPotsTTBB_7" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

datasets = [ "TOTEM_minBias_0T", "TOTEM_romanPots_0T", "ToTOTEM_0T", "ToTOTEM_DoubleJet32_0_0T", "ToTOTEM_DoubleJet32_1_0T",
             "ToTOTEM_DoubleJet32_2_0T", "ToTOTEM_DoubleJet32_3_0T", "TOTEM_zeroBias_0T", "ZeroBiasTotem_0T", "MinimumBiasTotem_0T",
             "TOTEM_minBias1_0T", "TOTEM_minBias2_0T", "TOTEM_romanPots1_0T", "TOTEM_romanPots2_0T", "TOTEM_romanPots2_0_0T",
             "TOTEM_romanPots2_1_0T", "TOTEM_romanPots2_2_0T", "TOTEM_romanPots2_3_0T", "TOTEM_romanPots2_4_0T",
             "TOTEM_romanPots2_5_0T", "TOTEM_romanPots2_6_0T", "TOTEM_romanPots2_7_0T", "TOTEM_romanPots3_0T",
             "TOTEM_romanPotsTTBB_0_0T", "TOTEM_romanPotsTTBB_1_0T", "TOTEM_romanPotsTTBB_2_0T", "TOTEM_romanPotsTTBB_3_0T",
             "TOTEM_romanPotsTTBB_4_0T", "TOTEM_romanPotsTTBB_5_0T", "TOTEM_romanPotsTTBB_6_0T", "TOTEM_romanPotsTTBB_7_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenarioB0T)

################################
### 50 ns Physics Menu       ###
################################

datasets = [ "BTagCSV" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               tape_node = "T1_UK_RAL_MSS",
               disk_node = "T1_UK_RAL_Disk",
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "BTagCSV_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               tape_node = "T1_UK_RAL_MSS",
               disk_node = "T1_UK_RAL_Disk",
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "DisplacedJet" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               raw_to_disk = True,
               dqm_sequences = [ "@common" ],
               tape_node = "T1_IT_CNAF_MSS",
               disk_node = "T1_IT_CNAF_Disk",
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "DisplacedJet_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               raw_to_disk = True,
               dqm_sequences = [ "@common" ],
               tape_node = "T1_IT_CNAF_MSS",
               disk_node = "T1_IT_CNAF_Disk",
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "MuonEG" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               tape_node = "T1_US_FNAL_MSS",
               disk_node = "T1_US_FNAL_Disk",
               physics_skims = [ "TopMuEG", "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "MuonEG_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               tape_node = "T1_US_FNAL_MSS",
               disk_node = "T1_US_FNAL_Disk",
               physics_skims = [ "TopMuEG", "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "DoubleMuonLowMass" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               tape_node = "T1_US_FNAL_MSS",
               disk_node = "T1_US_FNAL_Disk",
               physics_skims = [ "LogError", "LogErrorMonitor", "BPHSkim" ],
               scenario = ppScenario)

datasets = [ "DoubleMuonLowMass_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               tape_node = "T1_US_FNAL_MSS",
               disk_node = "T1_US_FNAL_Disk",
               physics_skims = [ "LogError", "LogErrorMonitor", "BPHSkim" ],
               scenario = ppScenarioB0T)

datasets = [ "HTMHT" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               raw_to_disk = True,
               dqm_sequences = [ "@common" ],
               tape_node = "T1_UK_RAL_MSS",
               disk_node = "T1_UK_RAL_Disk",
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               timePerEvent = 9.4,
               sizePerEvent = 2000,
               scenario = ppScenario)

datasets = [ "HTMHT_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               raw_to_disk = True,
               dqm_sequences = [ "@common" ],
               tape_node = "T1_UK_RAL_MSS",
               disk_node = "T1_UK_RAL_Disk",
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               timePerEvent = 9.4,
               sizePerEvent = 2000,
               scenario = ppScenarioB0T)

datasets = [ "Tau" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               raw_to_disk = True,
               dqm_sequences = [ "@common" ],
               tape_node = "T1_ES_PIC_MSS",
               disk_node = "T1_ES_PIC_Disk",
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "Tau_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               raw_to_disk = True,
               dqm_sequences = [ "@common" ],
               tape_node = "T1_ES_PIC_MSS",
               disk_node = "T1_ES_PIC_Disk",
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "BTagMu" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               tape_node = "T1_US_FNAL_MSS",
               disk_node = "T1_US_FNAL_Disk",
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "BTagMu_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               tape_node = "T1_US_FNAL_MSS",
               disk_node = "T1_US_FNAL_Disk",
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "Charmonium" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               tape_node = "T1_FR_CCIN2P3_MSS",
               disk_node = "T1_FR_CCIN2P3_Disk",
               alca_producers = [ "TkAlJpsiMuMu" ],
               physics_skims = [ "LogError", "LogErrorMonitor", "BPHSkim" ],
               scenario = ppScenario)

datasets = [ "Charmonium_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               tape_node = "T1_FR_CCIN2P3_MSS",
               disk_node = "T1_FR_CCIN2P3_Disk",
               alca_producers = [ "TkAlJpsiMuMu" ],
               physics_skims = [ "LogError", "LogErrorMonitor", "BPHSkim" ],
               scenario = ppScenarioB0T)

datasets = [ "DoubleEG" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               write_dqm = True,
               tape_node = "T1_UK_RAL_MSS",
               disk_node = "T1_UK_RAL_Disk",
               alca_producers = [ "EcalCalZElectron", "EcalUncalZElectron", "HcalCalIterativePhiSym", "HcalCalIsoTrkFilter" ],
               dqm_sequences = [ "@common", "@ecal", "@egamma" ],
               physics_skims = [ "ZElectron", "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "DoubleEG_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               write_dqm = True,
               tape_node = "T1_UK_RAL_MSS",
               disk_node = "T1_UK_RAL_Disk",
               alca_producers = [ "EcalCalZElectron", "EcalUncalZElectron", "HcalCalIterativePhiSym", "HcalCalIsoTrkFilter" ],
               dqm_sequences = [ "@common", "@ecal", "@egamma" ],
               physics_skims = [ "ZElectron", "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "SingleMu" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

datasets = [ "SingleMu_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenarioB0T)

datasets = [ "SingleMuon" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               tape_node = "T1_FR_CCIN2P3_MSS",
               disk_node = "T1_FR_CCIN2P3_Disk",
               alca_producers = [ "TkAlMuonIsolated", "HcalCalIterativePhiSym", "DtCalib", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu", "HcalCalHO", "HcalCalHBHEMuonFilter" ],
               dqm_sequences = [ "@common", "@muon" ],
               physics_skims = [ "ZMu", "MuTau", "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "SingleMuon_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               tape_node = "T1_FR_CCIN2P3_MSS",
               disk_node = "T1_FR_CCIN2P3_Disk",
               alca_producers = [ "TkAlMuonIsolated", "HcalCalIterativePhiSym", "DtCalib", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu", "HcalCalHO", "HcalCalHBHEMuonFilter" ],
               dqm_sequences = [ "@common", "@muon" ],
               physics_skims = [ "ZMu", "MuTau", "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "DoubleMu" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               alca_producers = [ "TkAlZMuMu", "TkAlJpsiMuMu", "TkAlUpsilonMuMu", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu", "DtCalib" , "HcalCalIsoTrkFilter" ],
               physics_skims = [ "Onia" ],
               scenario = ppScenario)

datasets = [ "DoubleMu_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               alca_producers = [ "TkAlZMuMu", "TkAlJpsiMuMu", "TkAlUpsilonMuMu", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu", "DtCalib", "HcalCalIsoTrkFilter" ],
               physics_skims = [ "Onia" ],
               scenario = ppScenarioB0T)

datasets = [ "DoubleMuon" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               tape_node = "T1_DE_KIT_MSS",
               disk_node = "T1_DE_KIT_Disk",
               alca_producers = [ "TkAlZMuMu", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu", "DtCalib" ],
               dqm_sequences = [ "@common", "@muon" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "DoubleMuon_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               tape_node = "T1_DE_KIT_MSS",
               disk_node = "T1_DE_KIT_Disk",
               alca_producers = [ "TkAlZMuMu", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu", "DtCalib" ],
               dqm_sequences = [ "@common", "@muon" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "JetHT" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               tape_node = "T1_DE_KIT_MSS",
               disk_node = "T1_DE_KIT_Disk",
               alca_producers = [ "HcalCalDijets", "HcalCalIsoTrkFilter", "HcalCalIsolatedBunchFilter" ],
               dqm_sequences = [ "@common", "@jetmet", "@hcal" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               timePerEvent = 5.7,
               sizePerEvent = 2250,
               scenario = ppScenario)

datasets = [ "JetHT_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               tape_node = "T1_DE_KIT_MSS",
               disk_node = "T1_DE_KIT_Disk",
               alca_producers = [ "HcalCalDijets", "HcalCalIsoTrkFilter", "HcalCalIsolatedBunchFilter" ],
               dqm_sequences = [ "@common", "@jetmet", "@hcal" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               timePerEvent = 5.7,
               sizePerEvent = 2250,
               scenario = ppScenarioB0T)

datasets = [ "MET" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               tape_node = "T1_DE_KIT_MSS",
               disk_node = "T1_DE_KIT_Disk",
               alca_producers = [ "HcalCalNoise" ],
               dqm_sequences = [ "@common", "@jetmet", "@hcal" ],
               physics_skims = [ "HighMET", "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "MET_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               tape_node = "T1_DE_KIT_MSS",
               disk_node = "T1_DE_KIT_Disk",
               alca_producers = [ "HcalCalNoise" ],
               dqm_sequences = [ "@common", "@jetmet", "@hcal" ],
               physics_skims = [ "HighMET", "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "MuOnia" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               tape_node = "T1_US_FNAL_MSS",
               disk_node = "T1_US_FNAL_Disk",
               alca_producers = [ "TkAlUpsilonMuMu" ],
               dqm_sequences = [ "@common", "@muon" ],
               physics_skims = [ "LogError", "LogErrorMonitor", "BPHSkim" ],
               scenario = ppScenario)

datasets = [ "MuOnia_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               tape_node = "T1_US_FNAL_MSS",
               disk_node = "T1_US_FNAL_Disk",
               alca_producers = [ "TkAlUpsilonMuMu" ],
               dqm_sequences = [ "@common", "@muon" ],
               physics_skims = [ "LogError", "LogErrorMonitor", "BPHSkim" ],
               scenario = ppScenarioB0T)

datasets = [ "SingleElectron" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               tape_node = "T1_IT_CNAF_MSS",
               disk_node = "T1_IT_CNAF_Disk",
               alca_producers = [ "EcalCalWElectron", "EcalUncalWElectron", "EcalCalZElectron", "EcalUncalZElectron", "HcalCalIterativePhiSym", "EcalESAlign", "HcalCalIsoTrkFilter" ],
               dqm_sequences = [ "@common", "@ecal", "@egamma" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "SingleElectron_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               tape_node = "T1_IT_CNAF_MSS",
               disk_node = "T1_IT_CNAF_Disk",
               alca_producers = [ "EcalCalWElectron", "EcalUncalWElectron", "EcalCalZElectron", "EcalUncalZElectron", "HcalCalIterativePhiSym", "EcalESAlign", "HcalCalIsoTrkFilter" ],
               dqm_sequences = [ "@common", "@ecal", "@egamma" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "TestEnablesEcalHcal" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               raw_to_disk = True,
               dqm_sequences = [ "@common" ],
               alca_producers = [ "HcalCalPedestal" ],
               scenario = ppScenario)

datasets = [ "TestEnablesEcalHcal_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               raw_to_disk = True,
               dqm_sequences = [ "@common" ],
               alca_producers = [ "HcalCalPedestal" ],
               scenario = ppScenarioB0T)

datasets = [ "SinglePhoton" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               tape_node = "T1_FR_CCIN2P3_MSS",
               disk_node = "T1_FR_CCIN2P3_Disk",
               alca_producers = [ "HcalCalGammaJet" ],
               dqm_sequences = [ "@common", "@ecal", "@egamma" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "SinglePhoton_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               tape_node = "T1_FR_CCIN2P3_MSS",
               disk_node = "T1_FR_CCIN2P3_Disk",
               alca_producers = [ "HcalCalGammaJet" ],
               dqm_sequences = [ "@common", "@ecal", "@egamma" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "DoublePhoton" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common", "@ecal", "@egamma" ],
               scenario = ppScenario)

datasets = [ "DoublePhoton_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common", "@ecal", "@egamma" ],
               scenario = ppScenarioB0T)

datasets = [ "HINPFJet100", "HINCaloJet100", "HighMultiplicity", "HighMultiplicityEOF" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

datasets = [ "HINPFJet100_0T", "HINCaloJet100_0T", "HighMultiplicity_0T", "HighMultiplicityEOF_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenarioB0T)

datasets = [ "HLTPhysicsCosmics", "HLTPhysicsCosmics1", "HLTPhysicsCosmics2",
            "HLTPhysicsCosmics3", "HLTPhysicsCosmics4", "HLTPhysicsCosmics5",
            "HLTPhysicsCosmics6", "HLTPhysicsCosmics7", "HLTPhysicsCosmics8" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               write_miniaod = False,
               scenario = cosmicsScenario)

datasets = [ "ParkingMonitor", "ParkingScoutingMonitor" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               write_reco = False, write_aod = False, write_miniaod = False, write_dqm = True,
               tape_node = "T1_US_FNAL_MSS",
               disk_node = None,
               scenario = ppScenario)

datasets = [ "ParkingMonitor_0T", "ParkingScoutingMonitor_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               write_reco = False, write_aod = False, write_miniaod = False, write_dqm = True,
               tape_node = "T1_US_FNAL_MSS",
               disk_node = None,
               scenario = ppScenarioB0T)
  
datasets = [ "ParkingHT410to430", "ParkingHT500to550", "ParkingHT430to450", "ParkingHT470to500", "ParkingHT450to470" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               write_reco = False,
               tape_node = "T1_RU_JINR_MSS",
               disk_node = None,
               scenario = ppScenario)

datasets = [ "ParkingHT410to430_0T", "ParkingHT500to550_0T", "ParkingHT430to450_0T", "ParkingHT470to500_0T", "ParkingHT450to470_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               write_reco = False, 
               tape_node = "T1_RU_JINR_MSS",
               disk_node = None,
               scenario = ppScenarioB0T)

datasets = [ "ParkingHT550to650", "ParkingHT650" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               write_reco = False,
               tape_node = "T1_US_FNAL_MSS",
               disk_node = None,
               scenario = ppScenario)

datasets = [ "ParkingHT550to650_0T", "ParkingHT650_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               write_reco = False,
               tape_node = "T1_US_FNAL_MSS",
               disk_node = None,
               scenario = ppScenarioB0T)
    
datasets = [ "ParkingHLTPhysics", "ParkingZeroBias", "AlCaPhiSym", "AlCaP0", 
             "AlCaElectron", "RPCMonitor", "VRRandom", "VRZeroBias", "VirginRaw" ]  

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               raw_to_disk = True,
               scenario = ppScenario)    
    
datasets = [ "ParkingHLTPhysics_0T", "ParkingZeroBias_0T", "AlCaPhiSym_0T", "AlCaP0_0T", 
             "AlCaElectron_0T", "RPCMonitor_0T", "VRRandom_0T", "VRZeroBias_0T", "VirginRaw_0T" ]  

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               raw_to_disk = True,
               scenario = ppScenarioB0T) 

#########################################
### New PDs for pp Reference Run 2015 ###
#########################################

datasets = [ "HighPtLowerPhotons", "HighPtPhoton30AndZ", "ppForward",
             "HighPtLowerJets", "MuPlusX" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

datasets = [ "HighPtLowerPhotons_0T", "HighPtPhoton30AndZ_0T", "ppForward_0T",
             "HighPtLowerJets_0T", "MuPlusX_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenarioB0T)

addDataset(tier0Config, "HeavyFlavor",
           do_reco = True,
           write_dqm = True,
           dqm_sequences = [ "@common" ],
           physics_skims = [ "D0Meson" ],
           scenario = ppScenario)

addDataset(tier0Config, "HeavyFlavor_0T",
           do_reco = True,
           write_dqm = True,
           dqm_sequences = [ "@common" ],
           physics_skims = [ "D0Meson" ],
           scenario = ppScenarioB0T)

addDataset(tier0Config, "HighPtJet80",
           do_reco = True,
           write_dqm = True,
           dqm_sequences = [ "@common" ],
           physics_skims = [ "HighPtJet" ],
           scenario = ppScenario)

addDataset(tier0Config, "HighPtJet80_0T",
           do_reco = True,
           write_dqm = True,
           dqm_sequences = [ "@common" ],
           physics_skims = [ "HighPtJet" ],
           scenario = ppScenarioB0T)

addDataset(tier0Config, "SingleMuHighPt",
           do_reco = True,
           write_dqm = True,
           dqm_sequences = [ "@common" ],
           alca_producers = [ "TkAlMuonIsolated", "HcalCalIterativePhiSym", "DtCalib", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu" ],
           physics_skims = [ "ZMM" ],
           scenario = ppScenario)

addDataset(tier0Config, "SingleMuHighPt_0T",
           do_reco = True,
           write_dqm = True,
           dqm_sequences = [ "@common" ],
           alca_producers = [ "TkAlMuonIsolated", "HcalCalIterativePhiSym", "DtCalib", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu" ],
           physics_skims = [ "ZMM" ],
           scenario = ppScenarioB0T)

addDataset(tier0Config, "SingleMuLowPt",
           do_reco = True,
           write_dqm = True,
           dqm_sequences = [ "@common" ],
           alca_producers = [ "TkAlMuonIsolated", "HcalCalIterativePhiSym", "DtCalib", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu" ],
           scenario = ppScenario)

addDataset(tier0Config, "SingleMuLowPt_0T",
           do_reco = True,
           write_dqm = True,
           dqm_sequences = [ "@common" ],
           alca_producers = [ "TkAlMuonIsolated", "HcalCalIterativePhiSym", "DtCalib", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu" ],
           scenario = ppScenarioB0T)

#########################################
### New PDs for PARun 2016 ###
#########################################

datasets = [ "PAHighMultiplicity0", "PAHighMultiplicity1", "PAHighMultiplicity2", "PAHighMultiplicity3",
             "PAHighMultiplicity4", "PAHighMultiplicity5", "PAHighMultiplicity6", "PAHighMultiplicity7" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               scenario = hiScenario)

addDataset(tier0Config, "PACastor",
           do_reco = True,
           write_dqm = True,
           dqm_sequences = [ "@common" ],
           scenario = hiScenario)

addDataset(tier0Config, "PAForward",
           do_reco = True,
           write_dqm = True,
           dqm_sequences = [ "@common" ],
           scenario = hiScenario)

addDataset(tier0Config, "PADoubleMuon",
           do_reco = True,
           write_dqm = True,
           dqm_sequences = [ "@common", "@muon" ],
           alca_producers = [ "TkAlMuonIsolatedPA", "TkAlZMuMuPA", "TkAlUpsilonMuMuPA", "DtCalib" ],
           scenario = hiScenario)

addDataset(tier0Config, "PASingleMuon",
           do_reco = True,
           write_dqm = True,
           dqm_sequences = [ "@common", "@muon" ],
           alca_producers = [ "TkAlMuonIsolatedPA", "DtCalib" ],
           physics_skims = [ "PAZMM" ],
           scenario = hiScenario)

datasets = [ "PADTrack1", "PADTrack2" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               scenario = hiScenario)

addDataset(tier0Config, "PAEGJet1",
           do_reco = True,
           write_dqm = True,
           dqm_sequences = [ "@common", "@ecal", "@egamma", "@hcal", "@jetmet" ],
           physics_skims = [ "PAZEE" ],
           scenario = hiScenario)

datasets = [ "PAMinimumBias1", "PAMinimumBias2", "PAMinimumBias3", "PAMinimumBias4", 
             "PAMinimumBias5", "PAMinimumBias6", "PAMinimumBias7", "PAMinimumBias8" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               alca_producers = [ "SiStripCalMinBias", "TkAlMinBias" ],
               scenario = hiScenario)

addDataset(tier0Config, "PAMinimumBiasBkg",
           do_reco = True,
           write_dqm = True,
           dqm_sequences = [ "@common" ],
           physics_skims = [ "PAMinBias" ],
           scenario = hiScenario)


addDataset(tier0Config, "PAEmptyBX",
           do_reco = True,
           write_dqm = True,
           dqm_sequences = [ "@common" ],
           scenario = hiScenario)

#############################
### Express configuration ###
#############################

addExpressConfig(tier0Config, "Express",
                 scenario = ppScenario,
                 data_tiers = [ "FEVT" ],
                 write_dqm = True,
                 alca_producers = [ "SiStripPCLHistos", "SiStripCalZeroBias", "SiStripCalMinBias", "SiStripCalMinBiasAfterAbortGap",
                                    "TkAlMinBias", "DtCalib", "PromptCalibProd", "Hotline", "LumiPixelsMinBias",
                                    "PromptCalibProdSiStrip", "PromptCalibProdSiStripGains", "PromptCalibProdSiPixelAli",
                                    "PromptCalibProdSiStripGainsAfterAbortGap" ],
                 reco_version = defaultCMSSWVersion,
                 multicore = numberOfCores,
                 global_tag_connect = globalTagConnect,
                 global_tag = expressGlobalTag,
                 proc_ver = expressProcVersion,
                 maxInputRate = 23 * 1000,
                 maxInputEvents = 400,
                 maxInputSize = 2 * 1024 * 1024 * 1024,
                 maxInputFiles = 15,
                 maxLatency = 15 * 23,
                 periodicHarvestInterval = 20 * 60,
                 blockCloseDelay = 1200,
                 timePerEvent = 4,
                 sizePerEvent = 1700,
                 versionOverride = expressVersionOverride)

addExpressConfig(tier0Config, "Express0T",
                 scenario = ppScenarioB0T,
                 data_tiers = [ "FEVT" ],
                 write_dqm = True,
                 alca_producers = [ "SiStripPCLHistos", "SiStripCalZeroBias", "SiStripCalMinBias", "SiStripCalMinBiasAfterAbortGap",
                                    "TkAlMinBias", "DtCalib", "PromptCalibProd", "Hotline", "LumiPixelsMinBias",
                                    "PromptCalibProdSiStrip", "PromptCalibProdSiStripGains", "PromptCalibProdSiPixelAli", 
                                    "PromptCalibProdSiStripGainsAfterAbortGap" ],
                 reco_version = defaultCMSSWVersion,
                 multicore = numberOfCores,
                 global_tag_connect = globalTagConnect,
                 global_tag = expressGlobalTag,
                 proc_ver = expressProcVersion,
                 maxInputRate = 23 * 1000,
                 maxInputEvents = 400,
                 maxInputSize = 2 * 1024 * 1024 * 1024,
                 maxInputFiles = 15,
                 maxLatency = 15 * 23,
                 periodicHarvestInterval = 20 * 60,
                 blockCloseDelay = 1200,
                 timePerEvent = 4,
                 sizePerEvent = 1700,
                 versionOverride = expressVersionOverride)

addExpressConfig(tier0Config, "ExpressCosmics",
                 scenario = cosmicsScenario,
                 data_tiers = [ "FEVT" ],
                 write_dqm = True,
                 alca_producers = [ "SiStripPCLHistos", "SiStripCalZeroBias", "TkAlCosmics0T",
                                    "PromptCalibProdSiStrip" ],
                 reco_version = defaultCMSSWVersion,
                 multicore = numberOfCores,
                 global_tag_connect = globalTagConnect,
                 global_tag = expressGlobalTag,
                 proc_ver = expressProcVersion,
                 maxInputRate = 23 * 1000,
                 maxInputEvents = 400,
                 maxInputSize = 2 * 1024 * 1024 * 1024,
                 maxInputFiles = 15,
                 maxLatency = 15 * 23,
                 periodicHarvestInterval = 20 * 60,
                 blockCloseDelay = 1200,
                 timePerEvent = 4, #I have to get some stats to set this properly
                 sizePerEvent = 1700, #I have to get some stats to set this properly
                 versionOverride = expressVersionOverride)

addExpressConfig(tier0Config, "HLTMonitor",
                 scenario = ppScenario,
                 data_tiers = [ "FEVTHLTALL" ],
                 write_dqm = True,
                 alca_producers = [],
                 dqm_sequences = [ "@HLTMon" ],
                 reco_version = defaultCMSSWVersion,
                 multicore = numberOfCores,
                 global_tag_connect = globalTagConnect,
                 global_tag = expressGlobalTag,
                 proc_ver = expressProcVersion,
                 maxInputRate = 23 * 1000,
                 maxInputEvents = 400,
                 maxInputSize = 2 * 1024 * 1024 * 1024,
                 maxInputFiles = 15,
                 maxLatency = 15 * 23,
                 periodicHarvestInterval = 20 * 60,
                 blockCloseDelay = 1200,
                 timePerEvent = 4, #I have to get some stats to set this properly
                 sizePerEvent = 1700, #I have to get some stats to set this properly
                 versionOverride = expressVersionOverride)

###############################
### ExpressPA configuration ###
###############################

addExpressConfig(tier0Config, "ExpressPA",
                 scenario = hiScenario,
                 data_tiers = [ "FEVT" ],
                 write_dqm = True,
                 alca_producers = [ "SiStripCalZeroBias", "TkAlMinBias", "DtCalib", "SiStripCalMinBias", 
                                    "SiStripCalMinBiasAfterAbortGap", "LumiPixelsMinBias", "PromptCalibProd",
                                    "PromptCalibProdSiStrip", "PromptCalibProdSiPixelAli", "PromptCalibProdSiStripGains", 
                                    "PromptCalibProdSiStripGainsAfterAbortGap", "SiStripPCLHistos" ],
                 reco_version = defaultCMSSWVersion,
                 multicore = numberOfCores,
                 global_tag_connect = globalTagConnect,
                 global_tag = expressGlobalTag,
                 proc_ver = expressProcVersion,
                 maxInputRate = 23 * 1000,
                 maxInputEvents = 400,
                 maxInputSize = 2 * 1024 * 1024 * 1024,
                 maxInputFiles = 15,
                 maxLatency = 15 * 23,
                 periodicHarvestInterval = 20 * 60,
                 blockCloseDelay = 1200,
                 timePerEvent = 4,
                 sizePerEvent = 1700,
                 versionOverride = expressVersionOverride)

addExpressConfig(tier0Config, "HLTMonitorPA",
                 scenario = hiScenario,
                 data_tiers = [ "FEVTHLTALL" ],
                 write_dqm = True,
                 alca_producers = [],
                 dqm_sequences = [ "@HLTMonPA" ],
                 reco_version = defaultCMSSWVersion,
                 multicore = numberOfCores,
                 global_tag_connect = globalTagConnect,
                 global_tag = expressGlobalTag,
                 proc_ver = expressProcVersion,
                 maxInputRate = 23 * 1000,
                 maxInputEvents = 400,
                 maxInputSize = 2 * 1024 * 1024 * 1024,
                 maxInputFiles = 15,
                 maxLatency = 15 * 23,
                 periodicHarvestInterval = 20 * 60,
                 blockCloseDelay = 1200,
                 timePerEvent = 4, #I have to get some stats to set this properly
                 sizePerEvent = 1700, #I have to get some stats to set this properly
                 versionOverride = expressVersionOverride)

#######################
### ignored streams ###
#######################

ignoreStream(tier0Config, "Error")
ignoreStream(tier0Config, "HLTMON")
ignoreStream(tier0Config, "EventDisplay")
ignoreStream(tier0Config, "DQM")
ignoreStream(tier0Config, "DQMEventDisplay")
ignoreStream(tier0Config, "LookArea")
ignoreStream(tier0Config, "DQMOffline")

###################################
### currently inactive settings ###
###################################

##ignoreStream(tier0Config, "Express")
##addRegistrationConfig(tier0Config, "UserStreamExample1",
##                      primds = "ExamplePrimDS1",
##                      acq_era = "AcqEra1",
##                      proc_string = "OptionalProcString",
##                      proc_version = "v1",
##                      data_tier = "RAW")
##
##addConversionConfig(tier0Config, "UserStreamExample",
##                    primds = "PrimDSTest6",
##                    acq_era = "AquEraTest6",
##                    proc_string = "ProcStringTest6",
##                    proc_version = "v6",
##                    data_tier = "RAW",
##                    conv_type = "streamer")

if __name__ == '__main__':
    print(tier0Config)
