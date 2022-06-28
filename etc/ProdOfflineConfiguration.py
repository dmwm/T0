"""
_OfflineConfiguration_

Processing configuration for the Tier0 - Production version
"""
from __future__ import print_function

from T0.RunConfig.Tier0Config import addDataset
from T0.RunConfig.Tier0Config import createTier0Config
from T0.RunConfig.Tier0Config import setAcquisitionEra
from T0.RunConfig.Tier0Config import setDefaultScramArch
from T0.RunConfig.Tier0Config import setBaseRequestPriority
from T0.RunConfig.Tier0Config import setBackfill
from T0.RunConfig.Tier0Config import setBulkDataType
from T0.RunConfig.Tier0Config import setProcessingSite
from T0.RunConfig.Tier0Config import setDQMDataTier
from T0.RunConfig.Tier0Config import setDQMUploadUrl
from T0.RunConfig.Tier0Config import setPromptCalibrationConfig
from T0.RunConfig.Tier0Config import setConfigVersion
from T0.RunConfig.Tier0Config import ignoreStream
from T0.RunConfig.Tier0Config import addRepackConfig
from T0.RunConfig.Tier0Config import addExpressConfig
from T0.RunConfig.Tier0Config import setInjectMinRun
from T0.RunConfig.Tier0Config import setInjectMaxRun
from T0.RunConfig.Tier0Config import setStreamerPNN
from T0.RunConfig.Tier0Config import addSiteConfig
from T0.RunConfig.Tier0Config import setStorageSite

# Create the Tier0 configuration object
tier0Config = createTier0Config()

# Set the verstion configuration (not used at the moment)
setConfigVersion(tier0Config, "replace with real version")

# Set the min run number:
setInjectMinRun(tier0Config, 351591)

# Set the max run number:
setInjectMaxRun(tier0Config, 9999999)

# Settings up sites
processingSite = "T2_CH_CERN"
storageSite = "T0_CH_CERN_Disk"
streamerPNN = "T0_CH_CERN_Disk"

addSiteConfig(tier0Config, "T0_CH_CERN_Disk",
                siteLocalConfig="/cvmfs/cms.cern.ch/SITECONF/T0_CH_CERN/JobConfig/site-local-config.xml",
                overrideCatalog="trivialcatalog_file:/cvmfs/cms.cern.ch/SITECONF/T0_CH_CERN/PhEDEx/storage.xml?protocol=eos"
                )

# Set global parameters:
#  Acquisition era
#  BaseRequestPriority
#  Backfill mode
#  Data type
#  Processing site (where jobs run)
#  PhEDEx locations
setAcquisitionEra(tier0Config, "Run2022A")
setBaseRequestPriority(tier0Config, 251000)
setBackfill(tier0Config, None)
setBulkDataType(tier0Config, "data")
setProcessingSite(tier0Config, processingSite)
setStreamerPNN(tier0Config, streamerPNN)
setStorageSite(tier0Config, storageSite)

# Override for DQM data tier
setDQMDataTier(tier0Config, "DQMIO")

# Define the two default timeouts for reco release
# First timeout is used directly for reco release
# Second timeout is used for the data service PromptReco start check
# (to basically say we started PromptReco even though we haven't)
defaultRecoTimeout = 48 * 3600
defaultRecoLockTimeout = 1800

# DQM Server
setDQMUploadUrl(tier0Config, "https://cmsweb.cern.ch/dqm/offline")

# PCL parameters
setPromptCalibrationConfig(tier0Config,
                           alcaHarvestTimeout=12*3600,
                           alcaHarvestCondLFNBase="/store/express/tier0_harvest",
                           alcaHarvestLumiURL="root://eoscms.cern.ch//eos/cms/tier0/store/unmerged/tier0_harvest",
                           conditionUploadTimeout=18*3600,
                           dropboxHost="webcondvm.cern.ch",
                           validationMode=False)

# Special syntax supported for cmssw version, processing version, global tag and processing scenario
# https://github.com/dmwm/T0/blob/master/src/python/T0/RunConfig/RunConfigAPI.py#L828
#
# { 'acqEra': {'Era1': Value1, 'Era2': Value2},
#   'maxRun': {100000: Value3, 200000: Value4},
#   'default': Value5 }

# Defaults for CMSSW version
defaultCMSSWVersion = {
    'default': "CMSSW_12_3_6"
}

# Configure ScramArch
setDefaultScramArch(tier0Config, "slc7_amd64_gcc10")

# Configure scenarios
ppScenario = "ppEra_Run3"
ppScenarioB0T = "ppEra_Run3"
cosmicsScenario = "cosmicsEra_Run3"
hcalnzsScenario = "hcalnzsEra_Run3"
hiScenario = "ppEra_Run3"
alcaTrackingOnlyScenario = "trackingOnlyEra_Run3"
alcaTestEnableScenario = "AlCaTestEnable"
alcaLumiPixelsScenario = "AlCaLumiPixels_Run3"
hiTestppScenario = "ppEra_Run3"

# Defaults for processing version
defaultProcVersionRAW = 1

alcarawProcVersion = {
    'default': "1"
}

defaultProcVersionReco = {
    'default': "1"
}

expressProcVersion = {
    'default': "1"
}

# Defaults for GlobalTag
expressGlobalTag = "123X_dataRun3_Express_v10"
promptrecoGlobalTag = "123X_dataRun3_Prompt_v12"
alcap0GlobalTag = "123X_dataRun3_Prompt_v12"

# Mandatory for CondDBv2
globalTagConnect = "frontier://PromptProd/CMS_CONDITIONS"

# Multicore settings
numberOfCores = 8

# Splitting parameters for PromptReco
defaultRecoSplitting = 750 * numberOfCores # reduced from 3000
hiRecoSplitting = 200 * numberOfCores
alcarawSplitting = 20000 * numberOfCores

#
# Setup repack and express mappings
#
repackVersionOverride = {
    "CMSSW_12_0_0" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_1" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_2" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_2_patch1" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_2_patch2" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_3" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_3_patch1" : defaultCMSSWVersion['default'],
    "CMSSW_12_2_1" : defaultCMSSWVersion['default'],
    "CMSSW_12_2_1_patch1" : defaultCMSSWVersion['default'],
    "CMSSW_12_2_2" : defaultCMSSWVersion['default'],
    "CMSSW_12_2_3" : defaultCMSSWVersion['default'],
    "CMSSW_12_2_3_patch1" : defaultCMSSWVersion['default'],
    "CMSSW_12_3_0" : defaultCMSSWVersion['default'],
    "CMSSW_12_3_2" : defaultCMSSWVersion['default'],
    "CMSSW_12_3_2_patch1" : defaultCMSSWVersion['default'],
    "CMSSW_12_3_3" : defaultCMSSWVersion['default'],
    "CMSSW_12_3_4" : defaultCMSSWVersion['default'],
    "CMSSW_12_3_4_patch2" : defaultCMSSWVersion['default'],
    "CMSSW_12_3_5" : defaultCMSSWVersion['default'],
    "CMSSW_12_3_5_patch1" : defaultCMSSWVersion['default'],
    "CMSSW_12_3_6" : defaultCMSSWVersion['default']
    }

expressVersionOverride = {
    "CMSSW_12_0_0" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_1" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_2" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_2_patch1" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_2_patch2" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_3" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_3_patch1" : defaultCMSSWVersion['default'],
    "CMSSW_12_2_1" : defaultCMSSWVersion['default'],
    "CMSSW_12_2_1_patch1" : defaultCMSSWVersion['default'],
    "CMSSW_12_2_2" : defaultCMSSWVersion['default'],
    "CMSSW_12_2_3" : defaultCMSSWVersion['default'],
    "CMSSW_12_2_3_patch1" : defaultCMSSWVersion['default'],
    "CMSSW_12_3_0" : defaultCMSSWVersion['default'],
    "CMSSW_12_3_2" : defaultCMSSWVersion['default'],
    "CMSSW_12_3_2_patch1" : defaultCMSSWVersion['default'],
    "CMSSW_12_3_3" : defaultCMSSWVersion['default'],
    "CMSSW_12_3_4" : defaultCMSSWVersion['default'],
    "CMSSW_12_3_4_patch2" : defaultCMSSWVersion['default'],
    "CMSSW_12_3_5" : defaultCMSSWVersion['default'],
    "CMSSW_12_3_5_patch1" : defaultCMSSWVersion['default'],
    "CMSSW_12_3_6" : defaultCMSSWVersion['default']
    }

#set default repack settings for bulk streams
addRepackConfig(tier0Config, "Default",
                proc_ver=defaultProcVersionRAW,
                maxSizeSingleLumi=24 * 1024 * 1024 * 1024,
                maxSizeMultiLumi=8 * 1024 * 1024 * 1024,
                minInputSize=2.1 * 1024 * 1024 * 1024,
                maxInputSize=4 * 1024 * 1024 * 1024,
                maxEdmSize=24 * 1024 * 1024 * 1024,
                maxOverSize=8 * 1024 * 1024 * 1024,
                maxInputEvents=3 * 1000 * 1000,
                maxInputFiles=1000,
                maxLatency=24 * 3600,
                blockCloseDelay=24 * 3600,
                maxMemory=2000,
                versionOverride=repackVersionOverride)

addDataset(tier0Config, "Default",
           do_reco=False,
           write_reco=False, write_aod=True, write_miniaod=True, write_dqm=False,
           reco_delay=defaultRecoTimeout,
           reco_delay_offset=defaultRecoLockTimeout,
           reco_split=defaultRecoSplitting,
           proc_version=defaultProcVersionReco,
           cmssw_version=defaultCMSSWVersion,
           multicore=numberOfCores,
           global_tag=promptrecoGlobalTag,
           global_tag_connect=globalTagConnect,
           archival_node="T0_CH_CERN_MSS",
           tape_node="T1_US_FNAL_MSS",
           disk_node="T1_US_FNAL_Disk",
           raw_to_disk=False,
           blockCloseDelay=24 * 3600,
           timePerEvent=5,
           sizePerEvent=1500,
           maxMemoryperCore=2000,
           dataset_lifetime=3*30*24*3600,#lifetime for container rules. Default 3 months
           scenario=ppScenario)

#############################
### Express configuration ###
#############################

addExpressConfig(tier0Config, "Express",
                 scenario=ppScenario,
                 diskNode="T2_CH_CERN",
                 data_tiers=["FEVT"],
                 write_dqm=True,
                 alca_producers=["SiStripPCLHistos", "SiStripCalZeroBias", "SiStripCalMinBias", "SiStripCalMinBiasAAG",
                                 "TkAlMinBias", "SiPixelCalZeroBias", "SiPixelCalSingleMuon",
                                 "PromptCalibProd", "PromptCalibProdSiStrip", "PromptCalibProdSiPixelAli",
                                 "PromptCalibProdSiStripGains", "PromptCalibProdSiStripGainsAAG", "PromptCalibProdSiPixel",
                                 "PromptCalibProdSiPixelLA", "PromptCalibProdSiStripHitEff"
                                ],
                 reco_version=defaultCMSSWVersion,
                 multicore=numberOfCores,
                 global_tag_connect=globalTagConnect,
                 global_tag=expressGlobalTag,
                 proc_ver=expressProcVersion,
                 maxInputRate=23 * 1000,
                 maxInputEvents=400,
                 maxInputSize=2 * 1024 * 1024 * 1024,
                 maxInputFiles=15,
                 maxLatency=15 * 23,
                 periodicHarvestInterval=20 * 60,
                 blockCloseDelay=1200,
                 timePerEvent=4,
                 sizePerEvent=1700,
                 maxMemoryperCore=2000,
                 dataset_lifetime=3*30*24*3600,#lifetime for container rules. Default 3 months
                 versionOverride=expressVersionOverride)

addExpressConfig(tier0Config, "ExpressCosmics",
                 scenario=cosmicsScenario,
                 diskNode="T2_CH_CERN",
                 data_tiers=["FEVT"],
                 write_dqm=True,
                 alca_producers=["SiStripPCLHistos", "SiStripCalZeroBias", "TkAlCosmics0T",
                                 "SiPixelCalZeroBias",
                                 "PromptCalibProdSiStrip"
                                ],
                 reco_version=defaultCMSSWVersion,
                 multicore=numberOfCores,
                 global_tag_connect=globalTagConnect,
                 global_tag=expressGlobalTag,
                 proc_ver=expressProcVersion,
                 maxInputRate=23 * 1000,
                 maxInputEvents=400,
                 maxInputSize=2 * 1024 * 1024 * 1024,
                 maxInputFiles=15,
                 maxLatency=15 * 23,
                 periodicHarvestInterval=20 * 60,
                 blockCloseDelay=1200,
                 timePerEvent=4, #I have to get some stats to set this properly
                 sizePerEvent=1700, #I have to get some stats to set this properly
                 maxMemoryperCore=2000,
                 dataset_lifetime=3*30*24*3600,#lifetime for container rules. Default 3 months
                 versionOverride=expressVersionOverride)

addExpressConfig(tier0Config, "HLTMonitor",
                 scenario=ppScenario,
                 diskNode="T2_CH_CERN",
                 data_tiers=["FEVTHLTALL"],
                 write_dqm=True,
                 alca_producers=[],
                 dqm_sequences=["@HLTMon"],
                 reco_version=defaultCMSSWVersion,
                 multicore=numberOfCores,
                 global_tag_connect=globalTagConnect,
                 global_tag=expressGlobalTag,
                 proc_ver=expressProcVersion,
                 maxInputRate=23 * 1000,
                 maxInputEvents=400,
                 maxInputSize=2 * 1024 * 1024 * 1024,
                 maxInputFiles=15,
                 maxLatency=15 * 23,
                 periodicHarvestInterval=20 * 60,
                 blockCloseDelay=1200,
                 timePerEvent=4, #I have to get some stats to set this properly
                 sizePerEvent=1700, #I have to get some stats to set this properly
                 maxMemoryperCore=2000,
                 dataset_lifetime=3*30*24*3600,#lifetime for container rules. Default 3 months
                 versionOverride=expressVersionOverride)

addExpressConfig(tier0Config, "Calibration",
                 scenario=alcaTestEnableScenario,
                 data_tiers=["RAW"],
                 write_dqm=True,
                 alca_producers=["EcalTestPulsesRaw", "PromptCalibProdEcalPedestals"],
                 reco_version=defaultCMSSWVersion,
                 multicore=numberOfCores,
                 global_tag_connect=globalTagConnect,
                 global_tag=expressGlobalTag,
                 proc_ver=expressProcVersion,
                 maxInputRate=23 * 1000,
                 maxInputEvents=100 * 1000 * 1000,
                 maxInputSize=4 * 1024 * 1024 * 1024,
                 maxInputFiles=10000,
                 maxLatency=1 * 3600,
                 periodicHarvestInterval=24 * 3600,
                 blockCloseDelay=2 * 3600,
                 timePerEvent=4,
                 sizePerEvent=1700,
                 versionOverride=expressVersionOverride,
                 maxMemoryperCore=2000,
                 archivalNode="T0_CH_CERN_MSS",
                 dataType="data",
                 dataset_lifetime=3*30*24*3600,#lifetime for container rules. Default 3 months
                 tape_node="T1_US_FNAL_MSS")

addExpressConfig(tier0Config, "ExpressAlignment",
                 scenario=alcaTrackingOnlyScenario,
                 data_tiers=["ALCARECO"],
                 write_dqm=True,
                 alca_producers=["TkAlMinBias", "PromptCalibProdBeamSpotHP"],
                 dqm_sequences=["@trackingOnlyDQM"],
                 reco_version=defaultCMSSWVersion,
                 multicore=numberOfCores,
                 global_tag_connect=globalTagConnect,
                 global_tag=expressGlobalTag,
                 proc_ver=expressProcVersion,
                 maxInputRate=23 * 1000,
                 maxInputEvents=100 * 1000 * 1000,
                 maxInputSize=4 * 1024 * 1024 * 1024,
                 maxInputFiles=10000,
                 maxLatency=1 * 3600,
                 periodicHarvestInterval=24 * 3600,
                 blockCloseDelay=2 * 3600,
                 timePerEvent=4,
                 sizePerEvent=1700,
                 versionOverride=expressVersionOverride,
                 maxMemoryperCore=2000,
                 dataset_lifetime=3*30*24*3600,#lifetime for container rules. Default 3 months
                 diskNode="T2_CH_CERN")

addExpressConfig(tier0Config, "ALCALumiPixelsCountsExpress",
                 scenario=alcaLumiPixelsScenario,
                 data_tiers=["ALCARECO"],
                 write_dqm=True,
                 alca_producers=["AlCaPCCRandom", "PromptCalibProdLumiPCC"],
                 dqm_sequences=[],
                 reco_version=defaultCMSSWVersion,
                 multicore=1,
                 global_tag_connect=globalTagConnect,
                 global_tag=expressGlobalTag,
                 proc_ver=expressProcVersion,
                 maxInputRate=23 * 1000,
                 maxInputEvents=100 * 1000 * 1000,
                 maxInputSize=4 * 1024 * 1024 * 1024,
                 maxInputFiles=10000,
                 maxLatency=1 * 3600,
                 periodicHarvestInterval=24 * 3600,
                 blockCloseDelay=2 * 3600,
                 timePerEvent=4,
                 sizePerEvent=1700,
                 versionOverride=expressVersionOverride,
                 maxMemoryperCore=2000,
                 archivalNode=None,
                 tapeNode=None,
                 dataset_lifetime=3*30*24*3600,#lifetime for container rules. Default 3 months
                 diskNode="T2_CH_CERN")


#####################
### HI Tests 2018 ###
#####################

addExpressConfig(tier0Config, "HIExpress",
                 scenario=hiTestppScenario,
                 diskNode="T2_CH_CERN",
                 data_tiers=["FEVT"],
                 write_dqm=True,
                 alca_producers=["SiStripPCLHistos", "SiStripCalZeroBias", "SiStripCalMinBias", "SiStripCalMinBiasAAG",
                                 "TkAlMinBias", "LumiPixelsMinBias", "SiPixelCalZeroBias",
                                 "PromptCalibProd", "PromptCalibProdSiStrip", "PromptCalibProdSiPixelAli",
                                 "PromptCalibProdSiStripGains", "PromptCalibProdSiStripGainsAAG", "PromptCalibProdSiPixel"
                                ],
                 reco_version=defaultCMSSWVersion,
                 multicore=numberOfCores,
                 global_tag_connect=globalTagConnect,
                 global_tag=expressGlobalTag,
                 proc_ver=expressProcVersion,
                 maxInputRate=23 * 1000,
                 maxInputEvents=400,
                 maxInputSize=2 * 1024 * 1024 * 1024,
                 maxInputFiles=15,
                 maxLatency=15 * 23,
                 periodicHarvestInterval=20 * 60,
                 blockCloseDelay=1200,
                 timePerEvent=4,
                 sizePerEvent=1700,
                 maxMemoryperCore=2000,
                 dataset_lifetime=3*30*24*3600,#lifetime for container rules. Default 3 months
                 versionOverride=expressVersionOverride)

addExpressConfig(tier0Config, "HIExpressAlignment",
                 scenario=hiTestppScenario,
                 data_tiers=["ALCARECO", "RAW"],
                 write_dqm=True,
                 alca_producers=["TkAlMinBias"],
                 dqm_sequences=["@trackingOnlyDQM"],
                 reco_version=defaultCMSSWVersion,
                 raw_to_disk=True,
                 multicore=numberOfCores,
                 global_tag_connect=globalTagConnect,
                 global_tag=expressGlobalTag,
                 proc_ver=expressProcVersion,
                 maxInputRate=23 * 1000,
                 maxInputEvents=100 * 1000 * 1000,
                 maxInputSize=4 * 1024 * 1024 * 1024,
                 maxInputFiles=10000,
                 maxLatency=1 * 3600,
                 periodicHarvestInterval=24 * 3600,
                 blockCloseDelay=2 * 3600,
                 timePerEvent=4,
                 sizePerEvent=1700,
                 versionOverride=expressVersionOverride,
                 maxMemoryperCore=2000,
                 dataset_lifetime=3*30*24*3600,#lifetime for container rules. Default 3 months
                 diskNode="T2_CH_CERN")

###################################
### Standard Physics PDs (2017) ###
###################################

DATASETS = ["BTagCSV"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               tape_node="T1_UK_RAL_MSS",
               disk_node="T1_UK_RAL_Disk",
               physics_skims=["LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["BTagMu"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               tape_node="T1_US_FNAL_MSS",
               disk_node="T1_US_FNAL_Disk",
               physics_skims=["LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["Charmonium"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False,
               raw_to_disk=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               tape_node="T1_US_FNAL_MSS",
               disk_node="T1_US_FNAL_Disk",
               alca_producers=["TkAlJpsiMuMu"],
               physics_skims=["BPHSkim", "MuonPOGJPsiSkim", "LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["Cosmics"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False,
               write_aod=True,
               write_miniaod=False,
               write_dqm=True,
               alca_producers=["SiStripCalCosmics", "SiPixelCalCosmics", "TkAlCosmics0T", "MuAlGlobalCosmics", "SiStripCalCosmicsNano"],
               physics_skims=["CosmicSP", "CosmicTP", "LogError", "LogErrorMonitor"],
               timePerEvent=0.5,
               sizePerEvent=155,
               scenario=cosmicsScenario)

DATASETS = ["DisplacedJet"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               tape_node="T1_FR_CCIN2P3_MSS",
               disk_node="T1_FR_CCIN2P3_Disk",
               physics_skims=["EXODisplacedJet", "LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["DoubleEG"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False,
               write_dqm=True,
               tape_node="T1_UK_RAL_MSS",
               disk_node="T1_UK_RAL_Disk",
               alca_producers=["EcalUncalZElectron", "EcalUncalWElectron", "HcalCalIterativePhiSym", "HcalCalIsoTrkProducerFilter"],
               dqm_sequences=["@common", "@ecal", "@egamma"],
               physics_skims=["ZElectron", "LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["DoubleMuon"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False,
               raw_to_disk=True,
               write_dqm=True,
               tape_node="T1_DE_KIT_MSS",
               disk_node="T1_DE_KIT_Disk",
               alca_producers=["TkAlZMuMu", "MuAlCalIsolatedMu", "TkAlDiMuonAndVertex"],
               dqm_sequences=["@common", "@muon", "@lumi", "@L1TMuon"],
               physics_skims=["LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["DoubleMuonLowPU"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False,
               raw_to_disk=True,
               write_dqm=True,
               tape_node="T1_DE_KIT_MSS",
               disk_node="T1_DE_KIT_Disk",
               alca_producers=["TkAlZMuMu", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu"],
               dqm_sequences=["@common", "@muon", "@lumi", "@L1TMuon"],
               physics_skims=["LogError", "LogErrorMonitor"],
               timePerEvent=1,
               scenario=ppScenario)

DATASETS = ["DoubleMuonLowMass"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common", "@muon"],
               alca_producers=["TkAlJpsiMuMu", "TkAlUpsilonMuMu"],
               physics_skims=["LogError", "LogErrorMonitor", "BPHSkim", "MuonPOGJPsiSkim"],
               tape_node="T1_US_FNAL_MSS",
               disk_node="T1_US_FNAL_Disk",
               scenario=ppScenario)

DATASETS = ["EmptyBX"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               scenario=ppScenario)

DATASETS = ["FSQJet1", "FSQJet2"]

DATASETS = ["FSQJets", "FSQJets1", "FSQJets2", "FSQJets3"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common", "@jetmet"],
               scenario=ppScenario)

DATASETS = ["HINCaloJets", "HINPFJets"]

DATASETS += ["HINCaloJet40", "HINPFJet100", "HINCaloJet100", "HINCaloJetsOther", "HINPFJetsOther"]

DATASETS += ["HINMuon", "HINPhoton"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               scenario=ppScenario)

DATASETS = ["HTMHT"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               tape_node="T1_UK_RAL_MSS",
               disk_node="T1_UK_RAL_Disk",
               physics_skims=["LogError", "LogErrorMonitor"],
               timePerEvent=9.4,
               sizePerEvent=2000,
               scenario=ppScenario)

DATASETS = ["HighMultiplicity"]

DATASETS += ["HighMultiplicityEOF0", "HighMultiplicityEOF1", "HighMultiplicityEOF2",
             "HighMultiplicityEOF3", "HighMultiplicityEOF4", "HighMultiplicityEOF5"]

DATASETS += ["HighMultiplicity85", "HighMultiplicity85EOF"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False,
               write_dqm=True,
               dqm_sequences=["@common"],
               scenario=ppScenario)

# 05/07/2018 HighMultiplicityEOF needs to have 1sec per event
DATASETS = ["HighMultiplicityEOF"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False,
               write_dqm=True,
               dqm_sequences=["@common"],
               timePerEvent=1,
               scenario=ppScenario)

DATASETS = ["HighPtLowerPhotons", "HighPtPhoton30AndZ"]

DATASETS += ["ppForward", "HighPtLowerJets", "MuPlusX"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               scenario=ppScenario)

DATASETS = ["JetHT"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               write_dqm=True,
               tape_node="T1_UK_RAL_MSS",
               disk_node="T1_UK_RAL_Disk",
               alca_producers=["HcalCalIsoTrkProducerFilter", "TkAlJetHT"],
               dqm_sequences=["@common", "@jetmet", "@L1TMon", "@hcal"],
               physics_skims=["JetHTJetPlusHOFilter", "LogError", "LogErrorMonitor"],
               timePerEvent=5.7,
               sizePerEvent=2250,
               scenario=ppScenario)

DATASETS = ["MET"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               write_dqm=True,
               tape_node="T1_DE_KIT_MSS",
               disk_node="T1_DE_KIT_Disk",
               alca_producers=["HcalCalNoise"],
               dqm_sequences=["@common", "@jetmet", "@L1TMon", "@hcal"],
               physics_skims=["EXOMONOPOLE", "HighMET", "LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["MuOnia"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               tape_node="T1_US_FNAL_MSS",
               disk_node="T1_US_FNAL_Disk",
               alca_producers=["TkAlUpsilonMuMu"],
               dqm_sequences=["@common", "@muon"],
               physics_skims=["LogError", "LogErrorMonitor", "BPHSkim"],
               scenario=ppScenario)

DATASETS = ["MuonEG"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               tape_node="T1_FR_CCIN2P3_MSS",
               disk_node="T1_FR_CCIN2P3_Disk",
               physics_skims=["TopMuEG", "LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["NoBPTX"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False,
               write_dqm=True,
               alca_producers=["TkAlCosmicsInCollisions"],
               dqm_sequences=["@common"],
               physics_skims=["EXONoBPTXSkim", "LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["SingleElectron"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               write_dqm=True,
               tape_node="T1_US_FNAL_MSS",
               disk_node="T1_US_FNAL_Disk",
               alca_producers=["EcalUncalWElectron", "EcalUncalZElectron", "HcalCalIterativePhiSym", "EcalESAlign"],
               dqm_sequences=["@common", "@ecal", "@egamma", "@L1TEgamma"],
               physics_skims=["LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["SingleMuon", "SingleMuonTnP"] # SingleMuonTnP only for 2017 ppRef run

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               write_dqm=True,
               tape_node="T1_US_FNAL_MSS", # "T1_IT_CNAF_MSS", CNAF is underwater
               disk_node="T1_US_FNAL_Disk", # "T1_IT_CNAF_Disk", CNAF is underwater
               alca_producers=["TkAlMuonIsolated", "HcalCalIterativePhiSym", "MuAlCalIsolatedMu",
                               "HcalCalHO", "HcalCalHBHEMuonProducerFilter",
                               "SiPixelCalSingleMuonLoose", "SiPixelCalSingleMuonTight"],
               dqm_sequences=["@common", "@muon", "@lumi", "@L1TMuon"],
               physics_skims=["MuonPOGSkim", "MuTau", "ZMu", "LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["SinglePhoton"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               write_dqm=True,
               tape_node="T1_FR_CCIN2P3_MSS",
               disk_node="T1_FR_CCIN2P3_Disk",
               dqm_sequences=["@common", "@ecal", "@egamma"],
               physics_skims=["EXOMONOPOLE", "LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["EGamma"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               write_dqm=True,
               tape_node="T1_IT_CNAF_MSS",
               disk_node="T1_IT_CNAF_Disk",
               alca_producers=["EcalUncalZElectron", "EcalUncalWElectron", "HcalCalIterativePhiSym",
                               "HcalCalIsoTrkProducerFilter", "EcalESAlign"],
               dqm_sequences=["@common", "@ecal", "@egamma", "@L1TEgamma"],
               physics_skims=["EXOMONOPOLE", "ZElectron", "LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["Tau"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               tape_node="T1_ES_PIC_MSS",
               disk_node="T1_ES_PIC_Disk",
               physics_skims=["LogError", "LogErrorMonitor"],
               scenario=ppScenario)

#############################################
### Standard Commisioning PDs (2017)      ###
#############################################

DATASETS = ["Commissioning"]

DATASETS += ["Commissioning1", "Commissioning2", "Commissioning3", "Commissioning4",
             "CommissioningMuons", "CommissioningEGamma", "CommissioningTaus", "CommissioningSingleJet", "CommissioningDoubleJet"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               write_dqm=True,
               alca_producers=["TkAlMinBias", "SiStripCalMinBias", "HcalCalIsoTrk", "HcalCalIsolatedBunchSelector"],
               dqm_sequences=["@common", "@L1TMon", "@hcal"],
               physics_skims=["EcalActivity", "LogError", "LogErrorMonitor"],
               timePerEvent=12,
               sizePerEvent=4000,
               scenario=ppScenario)

DATASETS = ["HcalNZS"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               write_aod=True,
               write_miniaod=True,
               write_reco=False,
               dqm_sequences=["@common", "@L1TMon", "@hcal"],
               alca_producers=["HcalCalMinBias"],
               physics_skims=["LogError", "LogErrorMonitor"],
               timePerEvent=4.2,
               sizePerEvent=1900,
               scenario=hcalnzsScenario)

DATASETS = ["TestEnablesEcalHcal", "TestEnablesEcalHcalDQM"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               raw_to_disk=True,
               alca_producers=["EcalTestPulsesRaw", "PromptCalibProdEcalPedestals", "HcalCalPedestal"],
               dqm_sequences=["@common"],
               scenario=alcaTestEnableScenario)

DATASETS = ["OnlineMonitor", "EcalLaser"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               raw_to_disk=False,
               scenario=ppScenario)

DATASETS = ["CosmicsForEventDisplay"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               raw_to_disk=False,
               write_miniaod=False,
               scenario=cosmicsScenario)

DATASETS = ["L1Accept", "L1Accepts"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               write_dqm=False,
               write_aod=True,
               write_miniaod=True,
               write_reco=False,
               dqm_sequences=["@common"],
               scenario=ppScenario)

###########################
### special AlcaRaw PDs ###
###########################

DATASETS = ["AlCaLumiPixels", "AlCaLumiPixels0", "AlCaLumiPixels1", "AlCaLumiPixels2", "AlCaLumiPixels3",
            "AlCaLumiPixels4", "AlCaLumiPixels5", "AlCaLumiPixels6", "AlCaLumiPixels7",
            "AlCaLumiPixels8", "AlCaLumiPixels9", "AlCaLumiPixels10", "AlCaLumiPixels11",
            "AlCaLumiPixels12"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False, write_aod=False, write_miniaod=False, write_dqm=True,
               disk_node=None,
               tape_node=None,
               reco_split=alcarawSplitting,
               proc_version=alcarawProcVersion,
               alca_producers=["AlCaPCCZeroBias"],
               dqm_sequences=["@common"],
               timePerEvent=0.02,
               sizePerEvent=38,
               scenario=alcaLumiPixelsScenario)

########################################################
### Pilot Tests PDs                                  ###
########################################################
DATASETS = ["AlCaLumiPixelsCountsPrompt0", "AlCaLumiPixelsCountsPrompt1", "AlCaLumiPixelsCountsPrompt2", "AlCaLumiPixelsCountsPrompt3",
            "AlCaLumiPixelsCountsPrompt4", "AlCaLumiPixelsCountsPrompt5", "AlCaLumiPixelsCountsPrompt6", "AlCaLumiPixelsCountsPrompt7",
            "AlCaLumiPixelsCountsPrompt8", "AlCaLumiPixelsCountsPrompt9", "AlCaLumiPixelsCountsPrompt10", "AlCaLumiPixelsCountsPrompt11",
            "AlCaLumiPixelsCountsPrompt12", "AlCaLumiPixelsCountsPrompt"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False, write_aod=False, write_miniaod=False, write_dqm=False,
               disk_node="T2_CH_CERN",
               tape_node=None,
               reco_split=alcarawSplitting,
               proc_version=alcarawProcVersion,
               alca_producers = [ "AlCaPCCZeroBias", "RawPCCProducer" ],
               timePerEvent=0.02,
               sizePerEvent=38,
               scenario=alcaLumiPixelsScenario)

DATASETS = ["AlCaLumiPixelsCountsExpress0", "AlCaLumiPixelsCountsExpress1", "AlCaLumiPixelsCountsExpress2", "AlCaLumiPixelsCountsExpress3",
            "AlCaLumiPixelsCountsExpress4", "AlCaLumiPixelsCountsExpress5", "AlCaLumiPixelsCountsExpress6", "AlCaLumiPixelsCountsExpress7",
            "AlCaLumiPixelsCountsExpress8", "AlCaLumiPixelsCountsExpress9", "AlCaLumiPixelsCountsExpress10", "AlCaLumiPixelsCountsExpress11",
            "AlCaLumiPixelsCountsExpress12", "AlCaLumiPixelsCountsExpress"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               write_reco=False, write_aod=False, write_miniaod=False, write_dqm=False,
               disk_node=None,
               tape_node=None,
               reco_split=alcarawSplitting,
               proc_version=alcarawProcVersion,
               timePerEvent=0.02,
               sizePerEvent=38,
               scenario=alcaLumiPixelsScenario)

DATASETS = ["AlCaPhiSym"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               raw_to_disk=True,
               alca_producers=["EcalCalPhiSym"],
               scenario=ppScenario)

DATASETS = ["AlCaP0"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               raw_to_disk=True,
               alca_producers=["EcalCalPi0Calib", "EcalCalEtaCalib"],
               scenario=ppScenario)

########################################################
### HLTPhysics PDs                                   ###
########################################################

DATASETS = ["HLTPhysics", "HLTPhysics0", "HLTPhysics1",
            "HLTPhysics2", "HLTPhysics3", "HLTPhysics4",
            "HLTPhysics5", "HLTPhysics6", "HLTPhysics7",
            "HLTPhysics8", "HLTPhysics9", "HLTPhysics10"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               write_reco=False,
               write_dqm=True,
               write_miniaod=True,
               write_aod=True,
               dqm_sequences=["@common", "@ecal", "@jetmet", "@L1TMon", "@hcal", "@L1TEgamma"],
               alca_producers=["TkAlMinBias"],
               physics_skims=["LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["HLTPhysicsBunchTrains", "HLTPhysicsIsolatedBunch"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               write_dqm=True,
               alca_producers=["SiStripCalMinBias", "TkAlMinBias", "HcalCalIsoTrkFilter"],
               physics_skims=["LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["HLTPhysicspart0", "HLTPhysicspart1",
            "HLTPhysicspart2", "HLTPhysicspart3", "HLTPhysicspart4",
            "HLTPhysicspart5", "HLTPhysicspart6", "HLTPhysicspart7"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               scenario=ppScenario)

DATASETS = ["EphemeralHLTPhysics1", "EphemeralHLTPhysics2", "EphemeralHLTPhysics3",
            "EphemeralHLTPhysics4", "EphemeralHLTPhysics5", "EphemeralHLTPhysics6",
            "EphemeralHLTPhysics7", "EphemeralHLTPhysics8"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               archival_node=None,
               tape_node=None,
               disk_node="T2_CH_CERN",
               scenario=ppScenario)

DATASETS = ["HLTPhysicsCosmics", "HLTPhysicsCosmics1", "HLTPhysicsCosmics2",
            "HLTPhysicsCosmics3", "HLTPhysicsCosmics4", "HLTPhysicsCosmics5",
            "HLTPhysicsCosmics6", "HLTPhysicsCosmics7", "HLTPhysicsCosmics8"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_miniaod=False,
               dqm_sequences=["@common"],
               scenario=cosmicsScenario)

########################################################
### MinimumBias PDs                                  ###
########################################################

DATASETS = ["MinimumBias", "MinimumBias0", "MinimumBias1", "MinimumBias2", "MinimumBias3",
            "MinimumBias4", "MinimumBias5", "MinimumBias6", "MinimumBias7",
            "MinimumBias8", "MinimumBias9", "MinimumBias10", "MinimumBias11",
            "MinimumBias12", "MinimumBias13", "MinimumBias14", "MinimumBias15",
            "MinimumBias16", "MinimumBias17", "MinimumBias18", "MinimumBias19",
            "MinimumBias20"
           ]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               tape_node="T1_US_FNAL_MSS",
               disk_node="T1_US_FNAL_Disk",
               dqm_sequences=["@commonSiStripZeroBias", "@ecal", "@L1TMon", "@hcal", "@muon", "@jetmet"],
               timePerEvent=1,
               alca_producers=["SiStripCalZeroBias", "SiStripCalMinBias", "TkAlMinBias", "HcalCalHO", 
                               "HcalCalIterativePhiSym", "HcalCalHBHEMuonProducerFilter", "HcalCalIsoTrkProducerFilter"],
               scenario=ppScenario)

DATASETS = ["L1MinimumBias"]

DATASETS += ["L1MinimumBiasHF1", "L1MinimumBiasHF2", "L1MinimumBiasHF3", "L1MinimumBiasHF4",
             "L1MinimumBiasHF5", "L1MinimumBiasHF6", "L1MinimumBiasHF7", "L1MinimumBiasHF8"]

DATASETS += ["L1MinimumBias0", "L1MinimumBias1", "L1MinimumBias2", "L1MinimumBias3", "L1MinimumBias4",
             "L1MinimumBias5", "L1MinimumBias6", "L1MinimumBias7", "L1MinimumBias8", "L1MinimumBias9",
             "L1MinimumBias10"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               scenario=ppScenario)

########################################################
### ZeroBias PDs                                     ###
########################################################

DATASETS = ["ZeroBias"]

DATASETS += ["ZeroBias1", "ZeroBias2",
             "ZeroBias3", "ZeroBias4", "ZeroBias5", "ZeroBias6",
             "ZeroBias7", "ZeroBias8", "ZeroBias9", "ZeroBias10",
             "ZeroBias11", "ZeroBias12", "ZeroBias13", "ZeroBias14",
             "ZeroBias15", "ZeroBias16", "ZeroBias17", "ZeroBias18",
             "ZeroBias19", "ZeroBias20"]

DATASETS += ["ZeroBiasIsolatedBunches", "ZeroBiasIsolatedBunches0", "ZeroBiasIsolatedBunches1", "ZeroBiasIsolatedBunches2",
             "ZeroBiasIsolatedBunches3", "ZeroBiasIsolatedBunches4", "ZeroBiasIsolatedBunches5", "ZeroBiasIsolatedBunches6",
             "ZeroBiasIsolatedBunches7", "ZeroBiasIsolatedBunches8", "ZeroBiasIsolatedBunches9", "ZeroBiasIsolatedBunches10"]

DATASETS += ["ZeroBiasIsolatedBunch", "ZeroBiasAfterIsolatedBunch",
             "ZeroBiasIsolatedBunch0", "ZeroBiasIsolatedBunch1", "ZeroBiasIsolatedBunch2",
             "ZeroBiasIsolatedBunch3", "ZeroBiasIsolatedBunch4", "ZeroBiasIsolatedBunch5"]

DATASETS += ["ZeroBiasBunchTrains0", "ZeroBiasBunchTrains1", "ZeroBiasBunchTrains2",
             "ZeroBiasBunchTrains3", "ZeroBiasBunchTrains4", "ZeroBiasBunchTrains5"]

DATASETS += ["ZeroBiasFirstBunchAfterTrain", "ZeroBiasFirstBunchInTrain"]

DATASETS += ["ZeroBiasPixelHVScan0", "ZeroBiasPixelHVScan1", "ZeroBiasPixelHVScan2",
             "ZeroBiasPixelHVScan3", "ZeroBiasPixelHVScan4", "ZeroBiasPixelHVScan5",
             "ZeroBiasPixelHVScan6", "ZeroBiasPixelHVScan7"]

DATASETS += ["ZeroBias8b4e1", "ZeroBias8b4e2", "ZeroBias8b4e3",
             "ZeroBias8b4e4", "ZeroBias8b4e5", "ZeroBias8b4e6",
             "ZeroBias8b4e7", "ZeroBias8b4e8", "ZeroBias8b4e10",
             "ZeroBias8b4e9"]

DATASETS += ["ZeroBiasNominalTrains1", "ZeroBiasNominalTrains2", "ZeroBiasNominalTrains3",
             "ZeroBiasNominalTrains4", "ZeroBiasNominalTrains5", "ZeroBiasNominalTrains6",
             "ZeroBiasNominalTrains7", "ZeroBiasNominalTrains8", "ZeroBiasNominalTrains10",
             "ZeroBiasNominalTrains9"]

DATASETS += ["ZeroBiasPD01", "ZeroBiasPD02", "ZeroBiasPD03",
             "ZeroBiasPD04", "ZeroBiasPD05", "ZeroBiasPD06",
             "ZeroBiasPD07", "ZeroBiasPD08", "ZeroBiasPD09",
             "ZeroBiasPD10"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               write_reco=False,
               write_dqm=True,
               dqm_sequences=["@commonSiStripZeroBias", "@ecal", "@L1TMon", "@hcal", "@muon", "@jetmet", "@ctpps"],
               alca_producers=["SiStripCalZeroBias", "TkAlMinBias", "SiStripCalMinBias"],
               physics_skims=["LogError", "LogErrorMonitor"],
               timePerEvent=3.5,
               sizePerEvent=1500,
               scenario=ppScenario)

DATASETS = ["ZeroBias0"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               write_reco=False,
               write_dqm=True,
               dqm_sequences=["@commonSiStripZeroBias", "@ecal", "@L1TMon", "@hcal", "@muon", "@jetmet", "@ctpps"],
               alca_producers=["SiStripCalZeroBias", "TkAlMinBias", "SiStripCalMinBias"],
               physics_skims=["LogError", "LogErrorMonitor"],
               siteWhitelist = ["T2_CH_CERN_HLT"],
               timePerEvent=3.5,
               sizePerEvent=1500,
               scenario=ppScenario)
    
DATASETS = ["EphemeralZeroBias1", "EphemeralZeroBias2", "EphemeralZeroBias3",
            "EphemeralZeroBias4", "EphemeralZeroBias5", "EphemeralZeroBias6",
            "EphemeralZeroBias7", "EphemeralZeroBias8"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               archival_node=None,
               tape_node=None,
               disk_node="T2_CH_CERN",
               scenario=ppScenario)

########################################################
### Parking and Scouting PDs                         ###
########################################################

DATASETS = ["ParkingMonitor"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               dqm_sequences=["@common"],
               write_reco=False, write_aod=False, write_miniaod=True, write_dqm=True,
               tape_node="T1_US_FNAL_MSS",
               disk_node=None,
               scenario=ppScenario)

DATASETS = ["ParkingScoutingMonitor"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               dqm_sequences=["@common"],
               write_reco=False, write_aod=False, write_miniaod=True, write_dqm=True,
               tape_node="T1_US_FNAL_MSS",
               scenario=ppScenario)

DATASETS = ["ParkingMuon", "ParkingHT"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               archival_node="T0_CH_CERN_MSS",
               tape_node=None,
               disk_node=None,
               scenario=ppScenario)

DATASETS = ["ParkingBPH1", "ParkingBPH2", "ParkingBPH3", "ParkingBPH4", "ParkingBPH5", "ParkingBPH6"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               archival_node="T0_CH_CERN_MSS",
               tape_node=None,
               disk_node=None,
               scenario=ppScenario)

# Parking PD to be PR'ed at CSCS
DATASETS = ["ParkingBPHPromptCSCS"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               siteWhitelist=["T0_CH_CSCS_HPC"],
               archival_node="T0_CH_CERN_MSS",
               tape_node=None,
               disk_node=None,
               scenario=ppScenario)

DATASETS = ["RPCMonitor"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               raw_to_disk=True,
               scenario=ppScenario)

DATASETS = ["ScoutingMonitor"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               dqm_sequences=["@common"],
               write_reco=False, write_aod=False, write_miniaod=True, write_dqm=True,
               tape_node="T1_US_FNAL_MSS",
               scenario=ppScenario)

DATASETS = ["ScoutingCaloCommissioning", "ScoutingCaloHT", "ScoutingCaloMuon",
            "ScoutingPFCommissioning", "ScoutingPFHT", "ScoutingPFMuon"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               raw_to_disk=True,
               scenario=ppScenario)

DATASETS = ["ParkingHT410to430", "ParkingHT500to550", "ParkingHT430to450", "ParkingHT470to500", "ParkingHT450to470"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               tape_node="T1_US_FNAL_MSS",
               disk_node=None,
               scenario=ppScenario)

DATASETS = ["ParkingHT550to650", "ParkingHT650"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               tape_node="T1_US_FNAL_MSS",
               disk_node=None,
               scenario=ppScenario)

DATASETS = ["ParkingHLTPhysics", "ParkingHLTPhysics0", "ParkingHLTPhysics1",
            "ParkingHLTPhysics2", "ParkingHLTPhysics3", "ParkingHLTPhysics4",
            "ParkingHLTPhysics5", "ParkingHLTPhysics6", "ParkingHLTPhysics7",
            "ParkingHLTPhysics8", "ParkingHLTPhysics9", "ParkingHLTPhysics10",
            "ParkingHLTPhysics11", "ParkingHLTPhysics12", "ParkingHLTPhysics13",
            "ParkingHLTPhysics14", "ParkingHLTPhysics15", "ParkingHLTPhysics16",
            "ParkingHLTPhysics17", "ParkingHLTPhysics18", "ParkingHLTPhysics19",
            "ParkingHLTPhysics20"]

DATASETS += ["ParkingZeroBias", "ParkingZeroBias0",
             "ParkingZeroBias1", "ParkingZeroBias2", "ParkingZeroBias3",
             "ParkingZeroBias4", "ParkingZeroBias5", "ParkingZeroBias6",
             "ParkingZeroBias7", "ParkingZeroBias8", "ParkingZeroBias9",
             "ParkingZeroBias10", "ParkingZeroBias11", "ParkingZeroBias12",
             "ParkingZeroBias13", "ParkingZeroBias14", "ParkingZeroBias15",
             "ParkingZeroBias16", "ParkingZeroBias17", "ParkingZeroBias18",
             "ParkingZeroBias19", "ParkingZeroBias20"]

DATASETS += ["AlCaElectron", "VRRandom", "VRRandom0", "VRRandom1", "VRRandom2", "VRRandom3",
             "VRRandom4", "VRRandom5", "VRRandom6", "VRRandom7", "VRRandom8", "VRRandom9",
             "VRRandom10", "VRRandom11", "VRRandom12", "VRRandom13", "VRRandom14", "VRRandom15",
             "VRZeroBias", "VirginRaw"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               raw_to_disk=True,
               scenario=ppScenario)


#########################################
### New PDs for pp Reference Run 2017 ###
#########################################

DATASETS = ["HighEGJet", "LowEGJet"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common", "@ecal", "@egamma", "@L1TMon", "@hcal", "@jetmet"],
               scenario=ppScenario)

DATASETS = ["HeavyFlavor", "SingleTrack"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               scenario=ppScenario)

DATASETS = ["HIZeroBias1", "HIZeroBias2", "HIZeroBias3", "HIZeroBias4",
            "HIZeroBias5", "HIZeroBias6", "HIZeroBias7", "HIZeroBias8",
            "HIZeroBias9", "HIZeroBias10", "HIZeroBias11", "HIZeroBias12"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@commonSiStripZeroBias", "@ecal", "@L1TMon", "@hcal", "@muon"],
               alca_producers=["SiStripCalZeroBias", "TkAlMinBias", "LumiPixelsMinBias", "SiStripCalMinBias", "AlCaPCCZeroBiasFromRECO"],
               timePerEvent=3.5,
               sizePerEvent=1500,
               scenario=ppScenario)

DATASETS = ["Totem12", "Totem34"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               dqm_sequences=["@common"],
               scenario=ppScenario)

################################
### Low PU collisions 13 TeV ###
################################

DATASETS = ["CastorJets", "EGMLowPU", "FullTrack"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               scenario=ppScenario)

DATASETS = ["HcalHPDNoise"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               dqm_sequences=["@common"],
               physics_skims=["LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["HINMuon_HFveto"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               dqm_sequences=["@common"],
               scenario=ppScenario)

################################
### Special Totem runs       ###
################################

DATASETS = ["TOTEM_minBias", "TOTEM_romanPots", "ToTOTEM", "ToTOTEM_DoubleJet32_0", "ToTOTEM_DoubleJet32_1",
            "ToTOTEM_DoubleJet32_2", "ToTOTEM_DoubleJet32_3", "TOTEM_zeroBias", "ZeroBiasTotem", "MinimumBiasTotem",
            "TOTEM_minBias1", "TOTEM_minBias2", "TOTEM_romanPots1", "TOTEM_romanPots2", "TOTEM_romanPots2_0",
            "TOTEM_romanPots2_1", "TOTEM_romanPots2_2", "TOTEM_romanPots2_3", "TOTEM_romanPots2_4",
            "TOTEM_romanPots2_5", "TOTEM_romanPots2_6", "TOTEM_romanPots2_7", "TOTEM_romanPots3",
            "TOTEM_romanPotsTTBB_0", "TOTEM_romanPotsTTBB_1", "TOTEM_romanPotsTTBB_2", "TOTEM_romanPotsTTBB_3",
            "TOTEM_romanPotsTTBB_4", "TOTEM_romanPotsTTBB_5", "TOTEM_romanPotsTTBB_6", "TOTEM_romanPotsTTBB_7"]

DATASETS += ["Totem1", "Totem2", "Totem3", "Totem4"]

### TOTEM DATASETS for 90m and LowPileUp menu - 2018/06/22
DATASETS += ["HFvetoTOTEM", "JetsTOTEM"]

DATASETS += ["RandomTOTEM1", "RandomTOTEM2", "RandomTOTEM3", "RandomTOTEM4"]

DATASETS += ["TOTEM10", "TOTEM11", "TOTEM12", "TOTEM13", "TOTEM20", "TOTEM21", "TOTEM22",
             "TOTEM23", "TOTEM3", "TOTEM40", "TOTEM41", "TOTEM42", "TOTEM43"]

DATASETS += ["ZeroBiasTOTEM1", "ZeroBiasTOTEM2", "ZeroBiasTOTEM3", "ZeroBiasTOTEM4"]
### TOTEM DATASETS for 90m and LowPileUp menu - 2018/06/22

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False,
               dqm_sequences=["@common"],
               scenario=ppScenario)

### TOTEM EGamma dataset for 90m and LowPileUp with egamma dqm sequence
DATASETS = ["MuonEGammaTOTEM"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False,
               write_dqm=True,
               dqm_sequences=["@common", "@egamma"],
               scenario=ppScenario)

# PPS 2022
DATASETS = ["AlCaPPS"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               scenario=ppScenario)

################################
### 50 ns Physics Menu       ###
################################

DATASETS = ["L1TechBPTXPlusOnly", "L1TechBPTXMinusOnly", "L1TechBPTXQuiet"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               dqm_sequences=["@common"],
               scenario=ppScenario)

DATASETS = ["SingleMu"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               dqm_sequences=["@common"],
               scenario=ppScenario)

DATASETS = ["DoubleMu"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               dqm_sequences=["@common"],
               alca_producers=["TkAlZMuMu", "TkAlJpsiMuMu", "TkAlUpsilonMuMu", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu", "HcalCalIsoTrkFilter"],
               physics_skims=["Onia"],
               scenario=ppScenario)

DATASETS = ["DoublePhoton"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common", "@ecal", "@egamma"],
               scenario=ppScenario)


#########################################
### New PDs for pp Reference Run 2015 ###
#########################################

# new PD with same name added for 2017 ppRef
# keeping this config for reference
# addDataset(tier0Config, "HeavyFlavor",
#            do_reco=True,
#            write_dqm=True,
#            dqm_sequences=["@common"],
#            physics_skims=["D0Meson"],
#            scenario=ppScenario)

addDataset(tier0Config, "HighPtJet80",
           do_reco=True,
           write_dqm=True,
           dqm_sequences=["@common"],
           physics_skims=["HighPtJet"],
           scenario=ppScenario)

addDataset(tier0Config, "SingleMuHighPt",
           do_reco=True,
           write_dqm=True,
           alca_producers=["TkAlMuonIsolated", "HcalCalIterativePhiSym", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu"],
           dqm_sequences=["@common"],
           physics_skims=["ZMM"],
           scenario=ppScenario)

addDataset(tier0Config, "SingleMuLowPt",
           do_reco=True,
           write_dqm=True,
           alca_producers=["TkAlMuonIsolated", "HcalCalIterativePhiSym", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu"],
           dqm_sequences=["@common"],
           scenario=ppScenario)

###############################
### ExpressPA configuration ###
###############################

addExpressConfig(tier0Config, "ExpressPA",
                 scenario=hiScenario,
                 data_tiers=["FEVT"],
                 write_dqm=True,
                 alca_producers=["SiStripCalZeroBias", "TkAlMinBias", "SiStripCalMinBias",
                                 "SiStripCalMinBiasAfterAbortGap", "LumiPixelsMinBias", "PromptCalibProd",
                                 "PromptCalibProdSiStrip", "PromptCalibProdSiPixelAli", "PromptCalibProdSiStripGains",
                                 "PromptCalibProdSiStripGainsAfterAbortGap", "SiStripPCLHistos"],
                 reco_version=defaultCMSSWVersion,
                 multicore=numberOfCores,
                 global_tag_connect=globalTagConnect,
                 global_tag=expressGlobalTag,
                 proc_ver=expressProcVersion,
                 maxInputRate=23 * 1000,
                 maxInputEvents=400,
                 maxInputSize=2 * 1024 * 1024 * 1024,
                 maxInputFiles=15,
                 maxLatency=15 * 23,
                 periodicHarvestInterval=20 * 60,
                 blockCloseDelay=1200,
                 timePerEvent=4,
                 sizePerEvent=1700,
                 diskNode="T2_CH_CERN",
                 versionOverride=expressVersionOverride)

addExpressConfig(tier0Config, "HLTMonitorPA",
                 scenario=hiScenario,
                 data_tiers=["FEVTHLTALL"],
                 write_dqm=True,
                 alca_producers=[],
                 dqm_sequences=["@HLTMonPA"],
                 reco_version=defaultCMSSWVersion,
                 multicore=numberOfCores,
                 global_tag_connect=globalTagConnect,
                 global_tag=expressGlobalTag,
                 proc_ver=expressProcVersion,
                 maxInputRate=23 * 1000,
                 maxInputEvents=400,
                 maxInputSize=2 * 1024 * 1024 * 1024,
                 maxInputFiles=15,
                 maxLatency=15 * 23,
                 periodicHarvestInterval=20 * 60,
                 blockCloseDelay=1200,
                 timePerEvent=4, #I have to get some stats to set this properly
                 sizePerEvent=1700, #I have to get some stats to set this properly
                 diskNode="T2_CH_CERN",
                 versionOverride=expressVersionOverride)

#########################################
### New PDs for PARun 2016 ###
#########################################

DATASETS = ["PAHighMultiplicity0", "PAHighMultiplicity1", "PAHighMultiplicity2", "PAHighMultiplicity3",
            "PAHighMultiplicity4", "PAHighMultiplicity5", "PAHighMultiplicity6", "PAHighMultiplicity7"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               scenario=hiScenario)

addDataset(tier0Config, "PACastor",
           do_reco=True,
           write_dqm=True,
           dqm_sequences=["@common"],
           scenario=hiScenario)

addDataset(tier0Config, "PAForward",
           do_reco=True,
           write_dqm=True,
           dqm_sequences=["@common"],
           scenario=hiScenario)

addDataset(tier0Config, "PADoubleMuon",
           do_reco=True,
           write_dqm=True,
           dqm_sequences=["@common", "@muon"],
           alca_producers=["TkAlMuonIsolatedPA", "TkAlZMuMuPA", "TkAlUpsilonMuMuPA"],
           scenario=hiScenario)

addDataset(tier0Config, "PASingleMuon",
           do_reco=True,
           write_dqm=True,
           dqm_sequences=["@common", "@muon"],
           alca_producers=["TkAlMuonIsolatedPA"],
           physics_skims=["PAZMM"],
           scenario=hiScenario)

DATASETS = ["PADTrack1", "PADTrack2"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               scenario=hiScenario)

addDataset(tier0Config, "PAEGJet1",
           do_reco=True,
           write_dqm=True,
           dqm_sequences=["@common", "@ecal", "@egamma", "@L1TMon", "@hcal", "@jetmet"],
           physics_skims=["PAZEE"],
           scenario=hiScenario)

DATASETS = ["PAMinimumBias1", "PAMinimumBias2", "PAMinimumBias3", "PAMinimumBias4",
            "PAMinimumBias5", "PAMinimumBias6", "PAMinimumBias7", "PAMinimumBias8",
            "PAMinimumBias9", "PAMinimumBias10", "PAMinimumBias11", "PAMinimumBias12",
            "PAMinimumBias13", "PAMinimumBias14", "PAMinimumBias15", "PAMinimumBias16",
            "PAMinimumBias17", "PAMinimumBias18", "PAMinimumBias19", "PAMinimumBias20"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               alca_producers=["SiStripCalMinBias", "TkAlMinBias"],
               scenario=hiScenario)

addDataset(tier0Config, "PAMinimumBiasBkg",
           do_reco=True,
           write_dqm=True,
           dqm_sequences=["@common"],
           physics_skims=["PAMinBias"],
           scenario=hiScenario)


addDataset(tier0Config, "PAEmptyBX",
           do_reco=True,
           write_dqm=True,
           dqm_sequences=["@common"],
           scenario=hiScenario)

#############################
###   PDs pA VdM scan     ###
#############################

DATASETS = ["PAL1AlwaysTrue0", "PAL1AlwaysTrue1", "PAL1AlwaysTrue2", "PAL1AlwaysTrue3",
            "PAL1AlwaysTrue4", "PAL1AlwaysTrue5", "PAL1AlwaysTrue6", "PAL1AlwaysTrue7",
            "PAL1AlwaysTrue8", "PAL1AlwaysTrue9"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               alca_producers=["LumiPixelsMinBias"],
               dqm_sequences=["@common"],
               scenario=hiScenario)

DATASETS = ["PAMinimumBiasHFOR0", "PAMinimumBiasHFOR1", "PAMinimumBiasHFOR2"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               alca_producers=["LumiPixelsMinBias"],
               dqm_sequences=["@common"],
               scenario=hiScenario)

DATASETS = ["PAZeroBias0", "PAZeroBias1", "PAZeroBias2", "PAZeroBias3",
            "PAZeroBias4", "PAZeroBias5", "PAZeroBias6", "PAZeroBias7",
            "PAZeroBias8", "PAZeroBias9"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               alca_producers=["LumiPixelsMinBias"],
               dqm_sequences=["@commonSiStripZeroBias", "@ecal", "@L1TMon", "@hcal", "@muon"],
               scenario=hiScenario)

addDataset(tier0Config, "PADoubleMuOpen",
           do_reco=True,
           write_dqm=True,
           alca_producers=["LumiPixelsMinBias"],
           dqm_sequences=["@common", "@muon"],
           scenario=hiScenario)

#####################
### HI TESTS 2018 ###
#####################

DATASETS = ["HITestFull", "HITestReduced"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               scenario=hiTestppScenario)

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
ignoreStream(tier0Config, "streamHLTRates")
ignoreStream(tier0Config, "streamL1Rates")
ignoreStream(tier0Config, "streamDQMRates")

###################################
### currently inactive settings ###
###################################

##ignoreStream(tier0Config, "Express")
##addRegistrationConfig(tier0Config, "UserStreamExample1",
##                      primds="ExamplePrimDS1",
##                      acq_era="AcqEra1",
##                      proc_string="OptionalProcString",
##                      proc_version="v1",
##                      data_tier="RAW")
##
##addConversionConfig(tier0Config, "UserStreamExample",
##                    primds="PrimDSTest6",
##                    acq_era="AquEraTest6",
##                    proc_string="ProcStringTest6",
##                    proc_version="v6",
##                    data_tier="RAW",
##                    conv_type="streamer")

if __name__ == '__main__':
    print(tier0Config)
