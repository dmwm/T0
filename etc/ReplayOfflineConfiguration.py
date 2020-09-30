"""
_OfflineConfiguration_
Processing configuration for the Tier0 - Replay version
"""
from __future__ import print_function

import os
import datetime
from T0.RunConfig.Tier0Config import addDataset
from T0.RunConfig.Tier0Config import createTier0Config
from T0.RunConfig.Tier0Config import setAcquisitionEra
from T0.RunConfig.Tier0Config import setScramArch
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
from T0.RunConfig.Tier0Config import addRegistrationConfig
from T0.RunConfig.Tier0Config import addConversionConfig
from T0.RunConfig.Tier0Config import setInjectRuns
from T0.RunConfig.Tier0Config import setStreamerPNN
from T0.RunConfig.Tier0Config import setEnableUniqueWorkflowName

# Create the Tier0 configuration object
tier0Config = createTier0Config()

# Set the verstion configuration (not used at the moment)
setConfigVersion(tier0Config, "replace with real version")

# Set run number to replay
setInjectRuns(tier0Config, [ 335508,336349,336436 ])

# Settings up sites
processingSite = "T2_CH_CERN"
streamerPNN = "T2_CH_CERN"

# Set global parameters:
#  Acquisition era
#  BaseRequestPriority
#  Backfill mode
#  Data type
#  Processing site (where jobs run)
#  PhEDEx locations
setAcquisitionEra(tier0Config, "Tier0_REPLAY_2020")
setBaseRequestPriority(tier0Config, 251000)
setBackfill(tier0Config, 1)
setBulkDataType(tier0Config, "data")
setProcessingSite(tier0Config, processingSite)
setStreamerPNN(tier0Config, streamerPNN)

# Override for DQM data tier
setDQMDataTier(tier0Config, "DQMIO")

# Set unique replay workflow names
# Uses era name, Repack, Express, PromptReco processing versions, date/time, e.g.:
# PromptReco_Run322057_Charmonium_Tier0_REPLAY_vocms047_v274_190221_121
setEnableUniqueWorkflowName(tier0Config)

# Define the two default timeouts for reco release
# First timeout is used directly for reco release
# Second timeout is used for the data service PromptReco start check
# (to basically say we started PromptReco even though we haven't)
defaultRecoTimeout =  10 * 60
defaultRecoLockTimeout = 5 * 60

# DQM Server
setDQMUploadUrl(tier0Config, "https://cmsweb.cern.ch/dqm/dev;https://cmsweb-testbed.cern.ch/dqm/offline-test")

# PCL parameters
setPromptCalibrationConfig(tier0Config,
                           alcaHarvestTimeout = 12*3600,
                           alcaHarvestCondLFNBase = "/store/unmerged/tier0_harvest",
                           alcaHarvestLumiURL = "root://eoscms.cern.ch//eos/cms/store/unmerged/tier0_harvest",
                           conditionUploadTimeout = 18*3600,
                           dropboxHost = "webcondvm.cern.ch",
                           validationMode = True)

# Special syntax supported for cmssw version, processing version and global tag
#
# { 'acqEra': {'Era1': Value1, 'Era2': Value2},
#   'maxRun': {100000: Value3, 200000: Value4},
#   'default': Value5 }

# Defaults for CMSSW version
defaultCMSSWVersion = {
       'default': "CMSSW_11_1_3"
     }

# Configure ScramArch
setDefaultScramArch(tier0Config, "slc7_amd64_gcc820")

# Configure scenarios
ppScenario = "ppEra_Run3"
ppScenarioB0T = "ppEra_Run3"
cosmicsScenario = "cosmicsEra_Run3"
hcalnzsScenario = "hcalnzsEra_Run3"
hiScenario = "ppEra_Run3"
alcaTrackingOnlyScenario = "trackingOnlyEra_Run2_2018"
alcaTestEnableScenario = "AlCaTestEnable"
alcaLumiPixelsScenario = "AlCaLumiPixels"
hiTestppScenario = "ppEra_Run3"

# Procesing version number replays
dt = int(datetime.datetime.now().strftime("%y%m%d%H%M"))
defaultProcVersion = dt
expressProcVersion = dt
alcarawProcVersion = dt

# Defaults for GlobalTag
expressGlobalTag = "111X_dataRun3_Express_v2"
promptrecoGlobalTag = "111X_dataRun3_Prompt_v2"
alcap0GlobalTag = "111X_dataRun3_Prompt_v2"

# Mandatory for CondDBv2
globalTagConnect = "frontier://PromptProd/CMS_CONDITIONS"

# Multicore settings
numberOfCores = 8

# Splitting parameters for PromptReco
defaultRecoSplitting = 750 * numberOfCores
hiRecoSplitting = 200 * numberOfCores
alcarawSplitting = 20000 * numberOfCores

#
# Setup repack and express mappings
#
repackVersionOverride = {
    "CMSSW_10_0_0" : "CMSSW_11_1_3",
    "CMSSW_10_0_1" : "CMSSW_11_1_3",
    "CMSSW_10_0_2" : "CMSSW_11_1_3",
    "CMSSW_10_0_3" : "CMSSW_11_1_3",
    "CMSSW_10_0_4" : "CMSSW_11_1_3",
    "CMSSW_10_0_5" : "CMSSW_11_1_3",
    "CMSSW_10_1_0" : "CMSSW_11_1_3",
    "CMSSW_10_1_1" : "CMSSW_11_1_3",
    "CMSSW_10_1_2" : "CMSSW_11_1_3",
    "CMSSW_10_1_3" : "CMSSW_11_1_3",
    "CMSSW_10_1_4" : "CMSSW_11_1_3",
    "CMSSW_10_1_5" : "CMSSW_11_1_3",
    "CMSSW_10_1_6" : "CMSSW_11_1_3",
    "CMSSW_10_1_7" : "CMSSW_11_1_3",
    "CMSSW_10_1_8" : "CMSSW_11_1_3",
    "CMSSW_10_1_9" : "CMSSW_11_1_3",
    "CMSSW_10_1_10" : "CMSSW_11_1_3",
    "CMSSW_10_2_0" : "CMSSW_11_1_3",
    "CMSSW_10_2_1" : "CMSSW_11_1_3",
    "CMSSW_10_2_5" : "CMSSW_11_1_3",
    "CMSSW_10_3_0" : "CMSSW_11_1_3",
    "CMSSW_10_3_1" : "CMSSW_11_1_3",
    "CMSSW_10_3_3" : "CMSSW_11_1_3",
    "CMSSW_10_6_1" : "CMSSW_11_1_3",
    "CMSSW_10_6_3" : "CMSSW_11_1_3",
    "CMSSW_10_6_8" : "CMSSW_11_1_3",
    "CMSSW_11_0_1" : "CMSSW_11_1_3",
    "CMSSW_11_0_2" : "CMSSW_11_1_3"
    }

expressVersionOverride = {
    "CMSSW_10_0_0" : "CMSSW_11_1_3",
    "CMSSW_10_0_1" : "CMSSW_11_1_3",
    "CMSSW_10_0_2" : "CMSSW_11_1_3",
    "CMSSW_10_0_3" : "CMSSW_11_1_3",
    "CMSSW_10_0_4" : "CMSSW_11_1_3",
    "CMSSW_10_0_5" : "CMSSW_11_1_3",
    "CMSSW_10_1_0" : "CMSSW_11_1_3",
    "CMSSW_10_1_1" : "CMSSW_11_1_3",
    "CMSSW_10_1_2" : "CMSSW_11_1_3",
    "CMSSW_10_1_3" : "CMSSW_11_1_3",
    "CMSSW_10_1_4" : "CMSSW_11_1_3",
    "CMSSW_10_1_5" : "CMSSW_11_1_3",
    "CMSSW_10_1_6" : "CMSSW_11_1_3",
    "CMSSW_10_1_7" : "CMSSW_11_1_3",
    "CMSSW_10_1_8" : "CMSSW_11_1_3",
    "CMSSW_10_1_9" : "CMSSW_11_1_3",
    "CMSSW_10_1_10" : "CMSSW_11_1_3",
    "CMSSW_10_2_0" : "CMSSW_11_1_3",
    "CMSSW_10_2_1" : "CMSSW_11_1_3",
    "CMSSW_10_2_5" : "CMSSW_11_1_3",
    "CMSSW_10_3_0" : "CMSSW_11_1_3",
    "CMSSW_10_3_1" : "CMSSW_11_1_3",
    "CMSSW_10_3_3" : "CMSSW_11_1_3",
    "CMSSW_10_6_1" : "CMSSW_11_1_3",
    "CMSSW_10_6_3" : "CMSSW_11_1_3",
    "CMSSW_10_6_8" : "CMSSW_11_1_3",
    "CMSSW_11_0_1" : "CMSSW_11_1_3",
    "CMSSW_11_0_2" : "CMSSW_11_1_3"

    }

#set default repack settings for bulk streams
addRepackConfig(tier0Config, "Default",
                proc_ver = defaultProcVersion,
                maxSizeSingleLumi = 24 * 1024 * 1024 * 1024,
                maxSizeMultiLumi = 8 * 1024 * 1024 * 1024,
                minInputSize =  2.1 * 1024 * 1024 * 1024,
                maxInputSize = 4 * 1024 * 1024 * 1024,
                maxEdmSize = 24 * 1024 * 1024 * 1024,
                maxOverSize = 8 * 1024 * 1024 * 1024,
                maxInputEvents = 3 * 1000 * 1000,
                maxInputFiles = 1000,
                maxLatency = 24 * 3600,
                blockCloseDelay = 1200,
                versionOverride = repackVersionOverride)

addDataset(tier0Config, "Default",
           do_reco = False,
           write_reco = False, write_aod = True, write_miniaod = True, write_dqm = False,
           reco_delay = defaultRecoTimeout,
           reco_delay_offset = defaultRecoLockTimeout,
           reco_split = defaultRecoSplitting,
           proc_version = defaultProcVersion,
           cmssw_version = defaultCMSSWVersion,
           multicore = numberOfCores,
           global_tag = promptrecoGlobalTag,
           global_tag_connect = globalTagConnect,
#           archival_node = "T0_CH_CERN_MSS",
#           tape_node = "T1_US_FNAL_MSS",
#           disk_node = "T1_US_FNAL_Disk",
#           raw_to_disk = False,
           blockCloseDelay = 1200,
           timePerEvent = 5,
           sizePerEvent = 1500,
           scenario = ppScenario)

#############################
### Express configuration ###
#############################

addExpressConfig(tier0Config, "Express",
                 scenario = ppScenario,
                 data_tiers = [ "FEVT" ],
                 write_dqm = True,
                 alca_producers = [ "SiStripPCLHistos", "SiStripCalZeroBias", "SiStripCalMinBias", "SiStripCalMinBiasAAG",
                                    "TkAlMinBias", "DtCalib", "LumiPixelsMinBias", "SiPixelCalZeroBias",
                                    "PromptCalibProd", "PromptCalibProdSiStrip", "PromptCalibProdSiPixelAli",
                                    "PromptCalibProdSiStripGains", "PromptCalibProdSiStripGainsAAG", "PromptCalibProdSiPixel"
                                    ],
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
                                    "DtCalibCosmics", "SiPixelCalZeroBias",
                                    "PromptCalibProdSiStrip", "PromptCalibProdSiPixel", "SiStripCalCosmics"
                                    ],
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

addExpressConfig(tier0Config, "Calibration",
                 scenario = alcaTestEnableScenario,
                 data_tiers = [ "RAW" ],
                 write_dqm = True,
                 alca_producers = [ "EcalTestPulsesRaw", "PromptCalibProdEcalPedestals" ],
                 reco_version = defaultCMSSWVersion,
                 multicore = numberOfCores,
                 global_tag_connect = globalTagConnect,
                 global_tag = expressGlobalTag,
                 proc_ver = expressProcVersion,
                 maxInputRate = 23 * 1000,
                 maxInputEvents = 100 * 1000 * 1000,
                 maxInputSize = 4 * 1024 * 1024 * 1024,
                 maxInputFiles = 10000,
                 maxLatency = 1 * 3600,
                 periodicHarvestInterval = 24 * 3600,
                 blockCloseDelay = 2 * 3600,
                 timePerEvent = 4,
                 sizePerEvent = 1700,
                 versionOverride = expressVersionOverride,
                 dataType = "data",
                 archivalNode = None,
                 tapeNode = None,
                 diskNode = None)

addExpressConfig(tier0Config, "ExpressAlignment",
                 scenario = alcaTrackingOnlyScenario,
                 data_tiers = [ "ALCARECO" ],
                 write_dqm = True,
                 alca_producers = [ "TkAlMinBias", "PromptCalibProdBeamSpotHP" ],
                 dqm_sequences = [ "DQMOfflineTracking" ],
                 reco_version = defaultCMSSWVersion,
                 multicore = numberOfCores,
                 global_tag_connect = globalTagConnect,
                 global_tag = expressGlobalTag,
                 proc_ver = expressProcVersion,
                 maxInputRate = 23 * 1000,
                 maxInputEvents = 100 * 1000 * 1000,
                 maxInputSize = 4 * 1024 * 1024 * 1024,
                 maxInputFiles = 10000,
                 maxLatency = 1 * 3600,
                 periodicHarvestInterval = 24 * 3600,
                 blockCloseDelay = 2 * 3600,
                 timePerEvent = 4,
                 sizePerEvent = 1700,
                 versionOverride = expressVersionOverride,
                 archivalNode = None,
                 tapeNode = None,
                 diskNode = None)

addExpressConfig(tier0Config, "ALCALUMIPIXELSEXPRESS",
                 scenario = alcaLumiPixelsScenario,
                 data_tiers = [ "ALCARECO" ],
                 write_dqm = True,
                 alca_producers = [ "AlCaPCCRandom", "PromptCalibProdLumiPCC" ],
                 dqm_sequences = [],
                 reco_version = defaultCMSSWVersion,
                 multicore = 1,
                 global_tag_connect = globalTagConnect,
                 global_tag = expressGlobalTag,
                 proc_ver = expressProcVersion,
                 maxInputRate = 23 * 1000,
                 maxInputEvents = 100 * 1000 * 1000,
                 maxInputSize = 4 * 1024 * 1024 * 1024,
                 maxInputFiles = 10000,
                 maxLatency = 1 * 3600,
                 periodicHarvestInterval = 24 * 3600,
                 blockCloseDelay = 2 * 3600,
                 timePerEvent = 4,
                 sizePerEvent = 1700,
                 versionOverride = expressVersionOverride,
                 archivalNode = None,
                 tapeNode = None,
                 diskNode = None)

#####################
### HI Tests 2018 ###
#####################

addExpressConfig(tier0Config, "HIExpress",
                 scenario = hiTestppScenario,
                 diskNode = "T2_CH_CERN",
                 data_tiers = [ "FEVT" ],
                 write_dqm = True,
                 alca_producers = [ "SiStripPCLHistos", "SiStripCalZeroBias", "SiStripCalMinBias", "SiStripCalMinBiasAAG",
                                    "TkAlMinBias", "DtCalib", "LumiPixelsMinBias", "SiPixelCalZeroBias",
                                    "PromptCalibProd", "PromptCalibProdSiStrip", "PromptCalibProdSiPixelAli",
                                    "PromptCalibProdSiStripGains", "PromptCalibProdSiStripGainsAAG", "PromptCalibProdSiPixel"
                                    ],
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

addExpressConfig(tier0Config, "HIExpressAlignment",
                 scenario = hiTestppScenario,
                 data_tiers = [ "ALCARECO", "RAW" ],
                 write_dqm = True,
                 alca_producers = [ "TkAlMinBias" ],
                 dqm_sequences = [ "DQMOfflineTracking" ],
                 reco_version = defaultCMSSWVersion,
                 raw_to_disk = True,
                 multicore = numberOfCores,
                 global_tag_connect = globalTagConnect,
                 global_tag = expressGlobalTag,
                 proc_ver = expressProcVersion,
                 maxInputRate = 23 * 1000,
                 maxInputEvents = 100 * 1000 * 1000,
                 maxInputSize = 4 * 1024 * 1024 * 1024,
                 maxInputFiles = 10000,
                 maxLatency = 1 * 3600,
                 periodicHarvestInterval = 24 * 3600,
                 blockCloseDelay = 2 * 3600,
                 timePerEvent = 4,
                 sizePerEvent = 1700,
                 versionOverride = expressVersionOverride,
                 diskNode = "T2_CH_CERN")

###################################
### Standard Physics PDs (2017) ###
###################################

datasets = [ "BTagCSV" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "BTagMu" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "Charmonium" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               alca_producers = [ "TkAlJpsiMuMu" ],
               physics_skims = [ "BPHSkim", "MuonPOGJPsiSkim", "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "Cosmics" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
           do_reco = True,
           write_reco = False,
           write_aod = True,
           write_miniaod = False,
           write_dqm = True,
           alca_producers = [ "TkAlCosmics0T", "MuAlGlobalCosmics", "DtCalibCosmics" ],
           physics_skims = [ "CosmicSP", "CosmicTP", "LogError", "LogErrorMonitor" ],
           timePerEvent = 0.5,
           sizePerEvent = 155,
           scenario = cosmicsScenario)

datasets = [ "DisplacedJet" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "EXODisplacedJet", "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "DoubleEG" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               write_dqm = True,
               alca_producers = [ "EcalUncalZElectron", "EcalUncalWElectron", "HcalCalIterativePhiSym", "HcalCalIsoTrkFilter" ],
               dqm_sequences = [ "@common", "@ecal", "@egamma" ],
               physics_skims = [ "ZElectron", "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "DoubleMuon" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               write_dqm = True,
               alca_producers = [ "TkAlZMuMu", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu", "DtCalib" ],
               dqm_sequences = [ "@common", "@muon", "@lumi", "@L1TMuon" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "DoubleMuonLowPU" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = False,
               raw_to_disk = True,
               write_dqm = True,
               alca_producers = [ "TkAlZMuMu", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu", "DtCalib" ],
               dqm_sequences = [ "@common", "@muon", "@lumi", "@L1TMuon" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               timePerEvent = 1,
               scenario = ppScenario)

datasets = [ "DoubleMuonLowMass" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "LogError", "LogErrorMonitor", "BPHSkim" ],
               scenario = ppScenario)

datasets = [ "EmptyBX" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

datasets = [ "FSQJet1", "FSQJet2" ]

datasets += [ "FSQJets", "FSQJets1", "FSQJets2", "FSQJets3" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common", "@jetmet" ],
               scenario = ppScenario)

datasets = [ "HINCaloJets", "HINPFJets" ]

datasets += [ "HINCaloJet40", "HINPFJet100", "HINCaloJet100", "HINCaloJetsOther", "HINPFJetsOther" ]

datasets += [ "HINMuon", "HINPhoton" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

datasets = [ "HTMHT" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               timePerEvent = 9.4,
               sizePerEvent = 2000,
               scenario = ppScenario)

datasets = [ "HighMultiplicity" ]

datasets += [ "HighMultiplicityEOF0", "HighMultiplicityEOF1", "HighMultiplicityEOF2",
              "HighMultiplicityEOF3", "HighMultiplicityEOF4", "HighMultiplicityEOF5" ]

datasets += [ "HighMultiplicity85", "HighMultiplicity85EOF" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

# 05/07/2018 HighMultiplicityEOF needs to have 1sec per event
datasets = [ "HighMultiplicityEOF" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = False,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               timePerEvent = 1,
               scenario = ppScenario)

datasets = [ "HighPtLowerPhotons", "HighPtPhoton30AndZ" ]

datasets += [ "ppForward", "HighPtLowerJets", "MuPlusX" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

datasets = [ "JetHT" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "HcalCalIsoTrkFilter", "HcalCalIsolatedBunchFilter" ],
               dqm_sequences = [ "@common", "@jetmet", "@hcal" ],
               physics_skims = [ "JetHTJetPlusHOFilter", "LogError", "LogErrorMonitor" ],
               timePerEvent = 5.7,
               sizePerEvent = 2250,
               scenario = ppScenario)

datasets = [ "MET" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "HcalCalNoise" ],
               dqm_sequences = [ "@common", "@jetmet", "@hcal" ],
               physics_skims = [ "EXOMONOPOLE", "HighMET", "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "MuOnia" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "TkAlUpsilonMuMu" ],
               dqm_sequences = [ "@common", "@muon" ],
               physics_skims = [ "LogError", "LogErrorMonitor", "BPHSkim" ],
               scenario = ppScenario)

datasets = [ "MuonEG" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "TopMuEG", "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "NoBPTX" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               write_dqm = True,
               alca_producers = [ "TkAlCosmicsInCollisions" ],
               dqm_sequences = [ "@common" ],
               physics_skims = [ "EXONoBPTXSkim", "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "SingleElectron" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "EcalUncalWElectron", "EcalUncalZElectron", "HcalCalIterativePhiSym", "EcalESAlign" ],
               dqm_sequences = [ "@common", "@ecal", "@egamma", "@L1TEgamma" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "SingleMuon", "SingleMuonTnP" ] # SingleMuonTnP only for 2017 ppRef run

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "TkAlMuonIsolated", "HcalCalIterativePhiSym", "DtCalib", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu", "HcalCalHO", "HcalCalHBHEMuonFilter" ],
               dqm_sequences = [ "@common", "@muon", "@lumi", "@L1TMuon" ],
               physics_skims = [ "MuonPOGSkim", "MuTau", "ZMu", "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "SinglePhoton" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common", "@ecal", "@egamma" ],
               physics_skims = [ "EXOMONOPOLE", "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "EGamma" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "EcalUncalZElectron", "EcalUncalWElectron", "HcalCalIterativePhiSym",
                "HcalCalIsoTrkFilter", "EcalESAlign" ],
               dqm_sequences = [ "@common", "@ecal", "@egamma", "@L1TEgamma" ],
               physics_skims = [ "EXOMONOPOLE", "ZElectron", "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "Tau" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

#############################################
### Standard Commisioning PDs (2017)      ###
#############################################

datasets = [ "Commissioning" ]

datasets += [ "Commissioning1", "Commissioning2", "Commissioning3", "Commissioning4",
              "CommissioningMuons", "CommissioningEGamma", "CommissioningTaus", "CommissioningSingleJet", "CommissioningDoubleJet"]

for dataset in datasets:
    addDataset(tier0Config, dataset,
           do_reco = True,
           write_dqm = True,
           alca_producers = [ "TkAlMinBias", "SiStripCalMinBias", "HcalCalIsoTrk", "HcalCalIsolatedBunchSelector" ],
           dqm_sequences = [ "@common", "@hcal" ],
           physics_skims = [ "EcalActivity", "LogError", "LogErrorMonitor" ],
           timePerEvent = 12,
           sizePerEvent = 4000,
           scenario = ppScenario)

datasets = [ "HcalNZS" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
           do_reco = True,
           write_dqm = True,
           write_aod = True,
           write_miniaod = True,
           write_reco = False,
           dqm_sequences = [ "@common", "@hcal" ],
           alca_producers = [ "HcalCalMinBias" ],
           physics_skims = [ "LogError", "LogErrorMonitor" ],
           timePerEvent = 4.2,
           sizePerEvent = 1900,
           scenario = hcalnzsScenario)

datasets = [ "TestEnablesEcalHcal", "TestEnablesEcalHcalDQM" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               alca_producers = [ "EcalTestPulsesRaw", "PromptCalibProdEcalPedestals" ],
               dqm_sequences = [ "@common" ],
               scenario = alcaTestEnableScenario)

datasets = [ "OnlineMonitor", "EcalLaser" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               scenario = ppScenario)

datasets = [ "CosmicsForEventDisplay" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               write_miniaod = False,
               scenario = cosmicsScenario)

datasets = [ "L1Accept", "L1Accepts" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               write_dqm = False,
               write_aod = True,
               write_miniaod = True,
               write_reco = False,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

###########################
### special AlcaRaw PDs ###
###########################

datasets = [ "AlCaLumiPixels" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
           do_reco = True,
           write_reco = False, write_aod = False, write_miniaod = False, write_dqm = True,
           reco_split = alcarawSplitting,
           proc_version = alcarawProcVersion,
           alca_producers = [ "AlCaPCCZeroBias" ],
           dqm_sequences = [ "@common" ],
           timePerEvent = 0.02,
           sizePerEvent = 38,
           scenario = alcaLumiPixelsScenario)

datasets = [ "AlCaLumiPixels0", "AlCaLumiPixels1", "AlCaLumiPixels2", "AlCaLumiPixels3",
             "AlCaLumiPixels4", "AlCaLumiPixels5", "AlCaLumiPixels6", "AlCaLumiPixels7",
             "AlCaLumiPixels8", "AlCaLumiPixels9", "AlCaLumiPixels10", "AlCaLumiPixels11",
             "AlCaLumiPixels12" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
           do_reco = True,
           write_reco = False, write_aod = False, write_miniaod = False, write_dqm = True,
           reco_split = alcarawSplitting,
           proc_version = alcarawProcVersion,
           alca_producers = [ "AlCaPCCZeroBias" ],
           dqm_sequences = [ "@common" ],
           timePerEvent = 0.02,
           sizePerEvent = 38,
           scenario = alcaLumiPixelsScenario)

datasets = [ "AlCaPhiSym" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               raw_to_disk = True,
               alca_producers = [ "EcalCalPhiSym" ],
               scenario = ppScenario)

datasets = [ "AlCaP0" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               raw_to_disk = True,
               alca_producers = [ "EcalCalPi0Calib", "EcalCalEtaCalib" ],
               scenario = ppScenario)

########################################################
### HLTPhysics PDs                                   ###
########################################################

datasets = [ "HLTPhysics" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = False,
               write_dqm = True,
               write_miniaod = True,
               write_aod = True,
               dqm_sequences = [ "@common", "@ecal", "@jetmet", "@hcal", "@L1TEgamma" ],
               alca_producers = [ "TkAlMinBias" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "HLTPhysics0", "HLTPhysics1", "HLTPhysics2",
             "HLTPhysics3", "HLTPhysics4", "HLTPhysics5",
             "HLTPhysics6", "HLTPhysics7", "HLTPhysics8",
             "HLTPhysics9", "HLTPhysics10" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common", "@ecal", "@jetmet", "@hcal", "@L1TEgamma" ],
               alca_producers = [ "TkAlMinBias" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "HLTPhysicsBunchTrains", "HLTPhysicsIsolatedBunch" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "SiStripCalMinBias", "TkAlMinBias", "HcalCalIsoTrkFilter" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "HLTPhysicspart0", "HLTPhysicspart1",
             "HLTPhysicspart2", "HLTPhysicspart3", "HLTPhysicspart4",
             "HLTPhysicspart5", "HLTPhysicspart6", "HLTPhysicspart7"  ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               scenario = ppScenario)

datasets = [ "EphemeralHLTPhysics1", "EphemeralHLTPhysics2", "EphemeralHLTPhysics3",
             "EphemeralHLTPhysics4", "EphemeralHLTPhysics5", "EphemeralHLTPhysics6",
             "EphemeralHLTPhysics7", "EphemeralHLTPhysics8"]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenario)

datasets = [ "HLTPhysicsCosmics", "HLTPhysicsCosmics1", "HLTPhysicsCosmics2",
            "HLTPhysicsCosmics3", "HLTPhysicsCosmics4", "HLTPhysicsCosmics5",
            "HLTPhysicsCosmics6", "HLTPhysicsCosmics7", "HLTPhysicsCosmics8" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_miniaod = False,
               dqm_sequences = [ "@common" ],
               scenario = cosmicsScenario)

########################################################
### MinimumBias PDs                                  ###
########################################################

datasets = [ "MinimumBias" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common", "@commonSiStripZeroBias", "@ecal", "@hcal", "@muon", "@jetmet" ],
               alca_producers = [ "SiStripCalZeroBias", "SiStripCalMinBias", "TkAlMinBias" ],
               scenario = ppScenario)

datasets = [ "MinimumBias0", "MinimumBias1", "MinimumBias2", "MinimumBias3",
             "MinimumBias4", "MinimumBias5", "MinimumBias6", "MinimumBias7",
             "MinimumBias8", "MinimumBias9", "MinimumBias10", "MinimumBias11",
             "MinimumBias12", "MinimumBias13", "MinimumBias14", "MinimumBias15",
             "MinimumBias16", "MinimumBias17", "MinimumBias18", "MinimumBias19",
             "MinimumBias20"
             ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common", "@commonSiStripZeroBias", "@ecal", "@hcal", "@muon", "@jetmet" ],
               timePerEvent = 1,
               alca_producers = [ "SiStripCalZeroBias", "SiStripCalMinBias", "TkAlMinBias" ],
               scenario = ppScenario)

datasets = [ "L1MinimumBias" ]

datasets += [ "L1MinimumBiasHF1", "L1MinimumBiasHF2", "L1MinimumBiasHF3", "L1MinimumBiasHF4",
              "L1MinimumBiasHF5", "L1MinimumBiasHF6", "L1MinimumBiasHF7", "L1MinimumBiasHF8" ]

datasets += [ "L1MinimumBias0", "L1MinimumBias1", "L1MinimumBias2", "L1MinimumBias3", "L1MinimumBias4",
              "L1MinimumBias5", "L1MinimumBias6", "L1MinimumBias7", "L1MinimumBias8", "L1MinimumBias9",
              "L1MinimumBias10" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

########################################################
### ZeroBias PDs                                     ###
########################################################

datasets = [ "ZeroBias" ]

datasets += [ "ZeroBias0", "ZeroBias1", "ZeroBias2",
             "ZeroBias3", "ZeroBias4", "ZeroBias5", "ZeroBias6",
             "ZeroBias7", "ZeroBias8", "ZeroBias9", "ZeroBias10",
             "ZeroBias11", "ZeroBias12", "ZeroBias13", "ZeroBias14",
             "ZeroBias15", "ZeroBias16", "ZeroBias17", "ZeroBias18",
             "ZeroBias19", "ZeroBias20" ]

datasets += [ "ZeroBiasIsolatedBunches", "ZeroBiasIsolatedBunches0", "ZeroBiasIsolatedBunches1", "ZeroBiasIsolatedBunches2",
             "ZeroBiasIsolatedBunches3", "ZeroBiasIsolatedBunches4", "ZeroBiasIsolatedBunches5", "ZeroBiasIsolatedBunches6",
             "ZeroBiasIsolatedBunches7", "ZeroBiasIsolatedBunches8", "ZeroBiasIsolatedBunches9", "ZeroBiasIsolatedBunches10" ]

datasets += [ "ZeroBiasIsolatedBunch", "ZeroBiasAfterIsolatedBunch",
             "ZeroBiasIsolatedBunch0", "ZeroBiasIsolatedBunch1", "ZeroBiasIsolatedBunch2",
             "ZeroBiasIsolatedBunch3", "ZeroBiasIsolatedBunch4", "ZeroBiasIsolatedBunch5" ]

datasets += [ "ZeroBiasBunchTrains0", "ZeroBiasBunchTrains1", "ZeroBiasBunchTrains2",
             "ZeroBiasBunchTrains3", "ZeroBiasBunchTrains4", "ZeroBiasBunchTrains5" ]

datasets += [ "ZeroBiasFirstBunchAfterTrain", "ZeroBiasFirstBunchInTrain" ]

datasets += [ "ZeroBiasPixelHVScan0", "ZeroBiasPixelHVScan1", "ZeroBiasPixelHVScan2",
             "ZeroBiasPixelHVScan3", "ZeroBiasPixelHVScan4", "ZeroBiasPixelHVScan5",
             "ZeroBiasPixelHVScan6", "ZeroBiasPixelHVScan7" ]

datasets += [ "ZeroBias8b4e1", "ZeroBias8b4e2", "ZeroBias8b4e3",
             "ZeroBias8b4e4", "ZeroBias8b4e5", "ZeroBias8b4e6",
             "ZeroBias8b4e7", "ZeroBias8b4e8", "ZeroBias8b4e10",
             "ZeroBias8b4e9" ]

datasets += [ "ZeroBiasNominalTrains1", "ZeroBiasNominalTrains2", "ZeroBiasNominalTrains3",
             "ZeroBiasNominalTrains4", "ZeroBiasNominalTrains5", "ZeroBiasNominalTrains6",
             "ZeroBiasNominalTrains7", "ZeroBiasNominalTrains8", "ZeroBiasNominalTrains10",
             "ZeroBiasNominalTrains9" ]

datasets += [ "ZeroBiasPD01", "ZeroBiasPD02", "ZeroBiasPD03",
             "ZeroBiasPD04", "ZeroBiasPD05", "ZeroBiasPD06",
             "ZeroBiasPD07", "ZeroBiasPD08", "ZeroBiasPD09",
             "ZeroBiasPD10"]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@commonSiStripZeroBias", "@ecal", "@hcal", "@muon", "@jetmet" ],
               alca_producers = [ "SiStripCalZeroBias", "TkAlMinBias", "LumiPixelsMinBias", "SiStripCalMinBias", "AlCaPCCZeroBiasFromRECO" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               timePerEvent = 3.5,
               sizePerEvent = 1500,
               scenario = ppScenario)

datasets = [ "EphemeralZeroBias1", "EphemeralZeroBias2", "EphemeralZeroBias3",
             "EphemeralZeroBias4", "EphemeralZeroBias5", "EphemeralZeroBias6",
             "EphemeralZeroBias7", "EphemeralZeroBias8"]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenario)

########################################################
### Parking and Scouting PDs                         ###
########################################################

datasets = [ "ParkingMonitor" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               write_reco = False, write_aod = False, write_miniaod = True, write_dqm = True,
               scenario = ppScenario)

datasets = [ "ParkingScoutingMonitor" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               write_reco = False, write_aod = False, write_miniaod = True, write_dqm = True,
               scenario = ppScenario)

datasets = [ "ParkingMuon", "ParkingHT" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               scenario = ppScenario)

datasets = [ "ParkingBPH1", "ParkingBPH2", "ParkingBPH3", "ParkingBPH4", "ParkingBPH5", "ParkingBPH6" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               tape_node = None,
               disk_node = None,
               scenario = ppScenario)

# Parking PD to be PR'ed at CSCS
datasets = [ "ParkingBPHPromptCSCS" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               siteWhitelist = [ "T0_CH_CSCS_HPC" ],
               scenario = ppScenario)

datasets = [ "RPCMonitor" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               scenario = ppScenario)

datasets = [ "ScoutingMonitor" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               write_reco = False, write_aod = False, write_miniaod = True, write_dqm = True,
               scenario = ppScenario)

datasets = [ "ScoutingCaloCommissioning", "ScoutingCaloHT", "ScoutingCaloMuon",
             "ScoutingPFCommissioning", "ScoutingPFHT", "ScoutingPFMuon" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               scenario = ppScenario)

datasets = [ "ParkingHT410to430", "ParkingHT500to550", "ParkingHT430to450", "ParkingHT470to500", "ParkingHT450to470" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               scenario = ppScenario)

datasets = [ "ParkingHT550to650", "ParkingHT650" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               scenario = ppScenario)

datasets = [ "ParkingHLTPhysics", "ParkingHLTPhysics0", "ParkingHLTPhysics1",
             "ParkingHLTPhysics2", "ParkingHLTPhysics3", "ParkingHLTPhysics4",
             "ParkingHLTPhysics5", "ParkingHLTPhysics6", "ParkingHLTPhysics7",
             "ParkingHLTPhysics8", "ParkingHLTPhysics9", "ParkingHLTPhysics10",
             "ParkingHLTPhysics11", "ParkingHLTPhysics12", "ParkingHLTPhysics13",
             "ParkingHLTPhysics14", "ParkingHLTPhysics15", "ParkingHLTPhysics16",
             "ParkingHLTPhysics17", "ParkingHLTPhysics18", "ParkingHLTPhysics19",
             "ParkingHLTPhysics20" ]

datasets += [ "ParkingZeroBias", "ParkingZeroBias0",
             "ParkingZeroBias1", "ParkingZeroBias2", "ParkingZeroBias3",
             "ParkingZeroBias4", "ParkingZeroBias5", "ParkingZeroBias6",
             "ParkingZeroBias7", "ParkingZeroBias8", "ParkingZeroBias9",
             "ParkingZeroBias10", "ParkingZeroBias11", "ParkingZeroBias12",
             "ParkingZeroBias13", "ParkingZeroBias14", "ParkingZeroBias15",
             "ParkingZeroBias16", "ParkingZeroBias17", "ParkingZeroBias18",
             "ParkingZeroBias19", "ParkingZeroBias20" ]

datasets += [ "AlCaElectron", "VRRandom", "VRRandom0", "VRRandom1", "VRRandom2", "VRRandom3",
             "VRRandom4", "VRRandom5", "VRRandom6", "VRRandom7", "VRZeroBias", "VirginRaw" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               scenario = ppScenario)

#########################################
### New PDs for pp Reference Run 2017 ###
#########################################

datasets = [ "HighEGJet", "LowEGJet" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common", "@ecal", "@egamma", "@hcal", "@jetmet" ],
               scenario = ppScenario)

datasets = [ "HeavyFlavor", "SingleTrack" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

datasets = [ "HIZeroBias1", "HIZeroBias2", "HIZeroBias3", "HIZeroBias4",
             "HIZeroBias5", "HIZeroBias6", "HIZeroBias7", "HIZeroBias8",
             "HIZeroBias9", "HIZeroBias10", "HIZeroBias11", "HIZeroBias12" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@commonSiStripZeroBias", "@ecal", "@hcal", "@muon" ],
               alca_producers = [ "SiStripCalZeroBias", "TkAlMinBias", "LumiPixelsMinBias", "SiStripCalMinBias", "AlCaPCCZeroBiasFromRECO" ],
               timePerEvent = 3.5,
               sizePerEvent = 1500,
               scenario = ppScenario)

datasets = [ "Totem12", "Totem34" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

################################
### Low PU collisions 13 TeV ###
################################

datasets = [ "CastorJets", "EGMLowPU", "FullTrack" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

datasets = [ "HcalHPDNoise" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "HINMuon_HFveto" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

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

datasets += [ "Totem1", "Totem2", "Totem3", "Totem4" ]

### TOTEM datasets for 90m and LowPileUp menu - 2018/06/22
datasets += [ "HFvetoTOTEM", "JetsTOTEM" ]

datasets += [ "RandomTOTEM1", "RandomTOTEM2", "RandomTOTEM3", "RandomTOTEM4" ]

datasets += [ "TOTEM10", "TOTEM11", "TOTEM12", "TOTEM13", "TOTEM20", "TOTEM21", "TOTEM22",
              "TOTEM23", "TOTEM3", "TOTEM40", "TOTEM41", "TOTEM42", "TOTEM43" ]

datasets += [ "ZeroBiasTOTEM1", "ZeroBiasTOTEM2", "ZeroBiasTOTEM3", "ZeroBiasTOTEM4" ]
### TOTEM datasets for 90m and LowPileUp menu - 2018/06/22

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

### TOTEM EGamma dataset for 90m and LowPileUp with egamma dqm sequence
datasets = [ "MuonEGammaTOTEM" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = False,
               write_dqm = True,
               dqm_sequences = [ "@common", "@egamma" ],
               scenario = ppScenario)

################################
### 50 ns Physics Menu       ###
################################

datasets = [ "L1TechBPTXPlusOnly", "L1TechBPTXMinusOnly", "L1TechBPTXQuiet" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

datasets = [ "SingleMu" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

datasets = [ "DoubleMu" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               alca_producers = [ "TkAlZMuMu", "TkAlJpsiMuMu", "TkAlUpsilonMuMu", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu", "DtCalib", "HcalCalIsoTrkFilter" ],
               physics_skims = [ "Onia" ],
               scenario = ppScenario)

datasets = [ "DoublePhoton" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common", "@ecal", "@egamma" ],
               scenario = ppScenario)


#########################################
### New PDs for pp Reference Run 2015 ###
#########################################

# new PD with same name added for 2017 ppRef
# keeping this config for reference
# addDataset(tier0Config, "HeavyFlavor",
#           do_reco = True,
#            write_dqm = True,
#            dqm_sequences = [ "@common" ],
#            physics_skims = [ "D0Meson" ],
#            scenario = ppScenario)

addDataset(tier0Config, "HighPtJet80",
           do_reco = True,
           write_dqm = True,
           dqm_sequences = [ "@common" ],
           physics_skims = [ "HighPtJet" ],
           scenario = ppScenario)

addDataset(tier0Config, "SingleMuHighPt",
           do_reco = True,
           write_dqm = True,
           alca_producers = [ "TkAlMuonIsolated", "HcalCalIterativePhiSym", "DtCalib", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu" ],
           dqm_sequences = [ "@common" ],
           physics_skims = [ "ZMM" ],
           scenario = ppScenario)

addDataset(tier0Config, "SingleMuLowPt",
           do_reco = True,
           write_dqm = True,
           alca_producers = [ "TkAlMuonIsolated", "HcalCalIterativePhiSym", "DtCalib", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu" ],
           dqm_sequences = [ "@common" ],
           scenario = ppScenario)

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
             "PAMinimumBias5", "PAMinimumBias6", "PAMinimumBias7", "PAMinimumBias8",
             "PAMinimumBias9", "PAMinimumBias10", "PAMinimumBias11", "PAMinimumBias12",
             "PAMinimumBias13", "PAMinimumBias14", "PAMinimumBias15", "PAMinimumBias16",
             "PAMinimumBias17", "PAMinimumBias18", "PAMinimumBias19", "PAMinimumBias20" ]

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
###   PDs pA VdM scan     ###
#############################

datasets = [ "PAL1AlwaysTrue0", "PAL1AlwaysTrue1", "PAL1AlwaysTrue2", "PAL1AlwaysTrue3",
             "PAL1AlwaysTrue4", "PAL1AlwaysTrue5", "PAL1AlwaysTrue6", "PAL1AlwaysTrue7",
             "PAL1AlwaysTrue8", "PAL1AlwaysTrue9" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "LumiPixelsMinBias" ],
               dqm_sequences = [ "@common" ],
               scenario = hiScenario)

datasets = [ "PAMinimumBiasHFOR0", "PAMinimumBiasHFOR1", "PAMinimumBiasHFOR2" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "LumiPixelsMinBias" ],
               dqm_sequences = [ "@common" ],
               scenario = hiScenario)

datasets = [ "PAZeroBias0", "PAZeroBias1", "PAZeroBias2", "PAZeroBias3",
             "PAZeroBias4", "PAZeroBias5", "PAZeroBias6", "PAZeroBias7",
             "PAZeroBias8", "PAZeroBias9" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "LumiPixelsMinBias" ],
               dqm_sequences = [ "@commonSiStripZeroBias", "@ecal", "@hcal", "@muon" ],
               scenario = hiScenario)

addDataset(tier0Config, "PADoubleMuOpen",
           do_reco = True,
           write_dqm = True,
           alca_producers = [ "LumiPixelsMinBias" ],
           dqm_sequences = [ "@common", "@muon" ],
           scenario = hiScenario)

#####################
### HI TESTS 2018 ###
#####################

datasets = [ "HITestFull", "HITestReduced" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               raw_to_disk = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               scenario = hiTestppScenario)

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
