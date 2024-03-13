"""
_OfflineConfiguration_
Processing configuration for the Tier0 - Replay version
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
from T0.RunConfig.Tier0Config import specifyStreams
from T0.RunConfig.Tier0Config import addRepackConfig
from T0.RunConfig.Tier0Config import addExpressConfig
from T0.RunConfig.Tier0Config import setInjectRuns
from T0.RunConfig.Tier0Config import setStreamerPNN
from T0.RunConfig.Tier0Config import setEnableUniqueWorkflowName
from T0.RunConfig.Tier0Config import addSiteConfig
from T0.RunConfig.Tier0Config import setStorageSite

# Create the Tier0 configuration object
tier0Config = createTier0Config()

# Set the verstion configuration (not used at the moment)
setConfigVersion(tier0Config, "replace with real version")

# Set run number to replay
# 352929 - 2022 pp at 900 GeV
# 355189 - 2022 cosmics
# 355559 - 2022 pp at 13.6 TeV (1h long, 300 bunches)
# 356005 - 2022 pp at 13.6 TeV (1h long, 600 bunches - ALL detectors included)
# 359060 - 2022 cosmics - Oberved failures in Express (https://cms-talk.web.cern.ch/t/paused-jobs-for-express-run359045-streamexpress/15232)
# 361694:361699,361779 - 2022 HI dry-run test runs
setInjectRuns(tier0Config, [375820])

# Settings up sites
processingSite = "T2_CH_CERN"
storageSite = "T0_CH_CERN_Disk"
streamerPNN = "T0_CH_CERN_Disk"

addSiteConfig(tier0Config, "T0_CH_CERN_Disk",
                siteLocalConfig="/cvmfs/cms.cern.ch/SITECONF/T0_CH_CERN/JobConfig/site-local-config.xml",
                overrideCatalog="T2_CH_CERN,,T0_CH_CERN,CERN_EOS_T0,XRootD"
                )

addSiteConfig(tier0Config, "EOS_PILOT",
                siteLocalConfig="/cvmfs/cms.cern.ch/SITECONF/T0_CH_CERN/JobConfig/site-local-config_EOS_PILOT.xml",
                overrideCatalog="trivialcatalog_file:/cvmfs/cms.cern.ch/SITECONF/T0_CH_CERN/PhEDEx/storage_EOS_PILOT.xml?protocol=eos"
                )

# Set global parameters:
#  Acquisition era
#  BaseRequestPriority
#  Backfill mode
#  Data type
#  Processing site (where jobs run)
#  PhEDEx locations
setAcquisitionEra(tier0Config, "Tier0_HIREPLAY_2023")
setBaseRequestPriority(tier0Config, 260000)
setBackfill(tier0Config, 1)
setBulkDataType(tier0Config, "hidata")
setProcessingSite(tier0Config, processingSite)
setStreamerPNN(tier0Config, streamerPNN)
setStorageSite(tier0Config, storageSite)

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
defaultRecoTimeout = 10 * 60
defaultRecoLockTimeout = 5 * 60

# DQM Server
setDQMUploadUrl(tier0Config, "https://cmsweb.cern.ch/dqm/dev;https://cmsweb-testbed.cern.ch/dqm/offline-test")

# PCL parameters
setPromptCalibrationConfig(tier0Config,
                           alcaHarvestTimeout=12*3600,
                           alcaHarvestCondLFNBase="/store/unmerged/tier0_harvest",
                           alcaHarvestLumiURL="root://eoscms.cern.ch//eos/cms/tier0/store/unmerged/tier0_harvest",
                           conditionUploadTimeout=18*3600,
                           dropboxHost="webcondvm.cern.ch",
                           validationMode=True)

# Special syntax supported for cmssw version, processing version and global tag
#
# { 'acqEra': {'Era1': Value1, 'Era2': Value2},
#   'maxRun': {100000: Value3, 200000: Value4},
#   'default': Value5 }

# Defaults for CMSSW version
defaultCMSSWVersion = {
    'default': "CMSSW_13_2_6_patch2"
}

# Configure ScramArch
setDefaultScramArch(tier0Config, "el8_amd64_gcc11")

# Configure scenarios
ppScenario = "ppEra_Run3_2023"
cosmicsScenario = "cosmicsEra_Run3"
hcalnzsScenario = "hcalnzsEra_Run3"
HIhcalnzsScenario = "hcalnzsEra_Run3_pp_on_PbPb"
hiScenario = "ppEra_Run3_pp_on_PbPb_2023"
alcaTrackingOnlyScenario = "trackingOnlyEra_Run3"
HIalcaTrackingOnlyScenario = "trackingOnlyEra_Run3_pp_on_PbPb"
alcaTestEnableScenario = "AlCaTestEnable"
alcaLumiPixelsScenario = "AlCaLumiPixels_Run3"
alcaPPSScenario = "AlCaPPS_Run3"
hiTestppScenario = "ppEra_Run3_pp_on_PbPb_2023"
hiRawPrimeScenario = "ppEra_Run3_pp_on_PbPb_approxSiStripClusters_2023"
hiForwardScenario = "ppEra_Run3_2023_repacked"

# Procesing version number replays
# Taking Replay processing ID from the last 8 digits of the DeploymentID
dt = int(open("/data/tier0/DeploymentID.txt","r").read()[4:])
defaultProcVersion = dt
expressProcVersion = dt
alcarawProcVersion = dt

# Defaults for GlobalTag
expressGlobalTag = "132X_dataRun3_Express_v4"
promptrecoGlobalTag = "132X_dataRun3_Prompt_v4"

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
    "CMSSW_12_6_3" : "CMSSW_12_6_4"
}

expressVersionOverride = {
    "CMSSW_12_6_3" : "CMSSW_12_6_4"
}

#set default repack settings for bulk streams
addRepackConfig(tier0Config, "Default",
                proc_ver=defaultProcVersion,
                maxSizeSingleLumi=24 * 1024 * 1024 * 1024,
                maxSizeMultiLumi=8 * 1024 * 1024 * 1024,
                minInputSize=2.1 * 1024 * 1024 * 1024,
                maxInputSize=4 * 1024 * 1024 * 1024,
                maxEdmSize=24 * 1024 * 1024 * 1024,
                maxOverSize=8 * 1024 * 1024 * 1024,
                maxInputEvents=3 * 1000 * 1000,
                maxInputFiles=1000,
                maxLatency=2 * 3600,
                blockCloseDelay=1200,
                maxMemory=2000,
                versionOverride=repackVersionOverride)

addDataset(tier0Config, "Default",
           do_reco=False,
           write_reco=False, write_aod=True, write_miniaod=True, write_nanoaod=False, write_dqm=False,
           reco_delay=defaultRecoTimeout,
           reco_delay_offset=defaultRecoLockTimeout,
           reco_split=defaultRecoSplitting,
           proc_version=defaultProcVersion,
           cmssw_version=defaultCMSSWVersion,
           multicore=numberOfCores,
           global_tag=promptrecoGlobalTag,
           global_tag_connect=globalTagConnect,
           #archival_node="T0_CH_CERN_MSS",
           tape_node="T0_CH_CERN_Disk",
           disk_node="T0_CH_CERN_Disk",
           #raw_to_disk=False,
           blockCloseDelay=1200,
           timePerEvent=5,
           sizePerEvent=1500,
           maxMemoryperCore=2000,
           dataset_lifetime=14*24*3600,#lifetime for container rules. Default 14 days
           scenario=ppScenario)

#############################
### Express configuration ###
#############################

addExpressConfig(tier0Config, "Express",
                 scenario=ppScenario,
                 diskNode="T0_CH_CERN_Disk",
                 data_tiers=["FEVT"],
                 write_dqm=True,
                 alca_producers=["SiStripPCLHistos", "SiStripCalZeroBias", "SiStripCalMinBias", "SiStripCalMinBiasAAG",
                                 "TkAlMinBias", "SiPixelCalZeroBias", "SiPixelCalSingleMuon", "SiPixelCalSingleMuonTight",
                                 "PromptCalibProd", "PromptCalibProdSiStrip", "PromptCalibProdSiPixelAli",
                                 "PromptCalibProdSiStripGains", "PromptCalibProdSiStripGainsAAG", "PromptCalibProdSiPixel",
                                 "PromptCalibProdSiPixelLA", "PromptCalibProdSiStripHitEff", "PromptCalibProdSiPixelAliHG"
                                ],
                 dqm_sequences=["@standardDQMExpress"],
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
                 dataset_lifetime=14*24*3600,#lifetime for container rules. Default 14 days
                 versionOverride=expressVersionOverride)

addExpressConfig(tier0Config, "ExpressCosmics",
                 scenario=cosmicsScenario,
                 diskNode="T0_CH_CERN_Disk",
                 data_tiers=["FEVT"],
                 write_dqm=True,
                 alca_producers=["SiStripPCLHistos", "SiStripCalZeroBias", "TkAlCosmics0T",
                                 "SiPixelCalZeroBias", "SiPixelCalCosmics", "SiStripCalCosmics",
                                 "PromptCalibProdSiStrip", "PromptCalibProdSiPixelLAMCS", "PromptCalibProdSiStripLA"
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
                 dataset_lifetime=14*24*3600,#lifetime for container rules. Default 14 days
                 versionOverride=expressVersionOverride)

addExpressConfig(tier0Config, "HLTMonitor",
                 scenario=ppScenario,
                 diskNode="T0_CH_CERN_Disk",
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
                 dataset_lifetime=14*24*3600,#lifetime for container rules. Default 14 days
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
                 dataType="hidata",
                 dataset_lifetime=14*24*3600,#lifetime for container rules. Default 14 days
                 diskNode="T0_CH_CERN_Disk")

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
                 dataset_lifetime=14*24*3600,#lifetime for container rules. Default 14 days
                 diskNode="T0_CH_CERN_Disk")

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
                 dataset_lifetime=14*24*3600,#lifetime for container rules. Default 14 days
                 diskNode="T0_CH_CERN_Disk")

addExpressConfig(tier0Config, "ALCAPPSExpress",
                 scenario=alcaPPSScenario,
                 data_tiers=["ALCARECO"],
                 dqm_sequences=["@none"],
                 write_dqm=True,
                 do_reco=False,
                 alca_producers=["PPSCalMaxTracks", "PromptCalibProdPPSTimingCalib", "PromptCalibProdPPSAlignment"],
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
                 dataset_lifetime=14*24*3600,#lifetime for container rules. Default 14 days
                 diskNode="T0_CH_CERN_Disk",
                 versionOverride=expressVersionOverride)

#####################
### HI Tests 2022 ###
#####################

addExpressConfig(tier0Config, "HIExpress",
                 scenario=hiTestppScenario,
                 diskNode="T0_CH_CERN_Disk",
                 data_tiers=["FEVT"],
                 write_dqm=True,
                 alca_producers=["SiStripPCLHistos", "SiStripCalZeroBias", "SiStripCalMinBias", "SiStripCalMinBiasAAG",
                                 "TkAlMinBias", "SiPixelCalZeroBias","SiPixelCalSingleMuon", "SiPixelCalSingleMuonTight",
                                 "SiPixelCalSingleMuonLoose",
                                 "PromptCalibProd", "PromptCalibProdSiStrip", "PromptCalibProdSiPixelAli",
                                 "PromptCalibProdSiStripGains", "PromptCalibProdSiStripGainsAAG", "PromptCalibProdSiPixel",
                                 "PromptCalibProdSiPixelLA", "PromptCalibProdSiStripHitEff", "PromptCalibProdSiPixelAliHG"
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
                 dataset_lifetime=14*24*3600,#lifetime for container rules. Default 14 days
                 versionOverride=expressVersionOverride)

addExpressConfig(tier0Config, "HIExpressRawPrime",
                 scenario=hiRawPrimeScenario,
                 diskNode="T2_CH_CERN",
                 data_tiers=["FEVT"],
                 write_dqm=True,
                 alca_producers=["SiStripCalMinBias", "SiStripCalMinBiasAAG"],
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
                 scenario=HIalcaTrackingOnlyScenario,
                 data_tiers=["ALCARECO", "RAW"],
                 write_dqm=True,
                 alca_producers=["TkAlMinBias", "PromptCalibProdBeamSpotHP"],
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
                 dataset_lifetime=14*24*3600,#lifetime for container rules. Default 14 days
                 diskNode="T0_CH_CERN_Disk")

addExpressConfig(tier0Config, "HIHLTMonitor",
                 scenario=hiTestppScenario,
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
                 timePerEvent=4,
                 sizePerEvent=1700,
                 dataset_lifetime=14*24*3600,#lifetime for container rules. Default 14 days
                 versionOverride=expressVersionOverride)

###################################
### Standard Physics PDs (2022) ###
###################################

DATASETS = ["BTagMu"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               physics_skims=["LogError", "LogErrorMonitor"],
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
               write_dqm=True,
               dqm_sequences=["@common"],
               physics_skims=["EXODisplacedJet", "EXODelayedJet", "EXODTCluster", "LogError", "LogErrorMonitor", "EXOLLPJetHCAL"],
               scenario=ppScenario)

DATASETS = ["DoubleMuon"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False,
               write_dqm=True,
               alca_producers=["TkAlZMuMu", "MuAlCalIsolatedMu", "TkAlDiMuonAndVertex"],
               dqm_sequences=["@common", "@muon", "@lumi", "@L1TMuon"],
               physics_skims=["LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["DoubleMuonLowPU"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False,
               write_dqm=True,
               alca_producers=["TkAlZMuMu", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu"],
               dqm_sequences=["@common", "@muon", "@lumi", "@L1TMuon"],
               physics_skims=["LogError", "LogErrorMonitor"],
               timePerEvent=1,
               scenario=ppScenario)

DATASETS = ["ReservedDoubleMuonLowMass"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               scenario=ppScenario)

DATASETS = ["ParkingSingleMuon","ParkingSingleMuon0"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               scenario=ppScenario)

DATASETS = ["ParkingSingleMuon1","ParkingSingleMuon2"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               aod_to_disk=False,
               archival_node=None,
               scenario=ppScenario)

DATASETS = ["ParkingDoubleMuonLowMass0"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common", "@muon", "@heavyFlavor"],
               alca_producers=["TkAlJpsiMuMu", "TkAlUpsilonMuMu"],
               archival_node=None,
               scenario=ppScenario)

DATASETS = ["ParkingDoubleMuonLowMass1","ParkingDoubleMuonLowMass2",
            "ParkingDoubleMuonLowMass3","ParkingDoubleMuonLowMass4","ParkingDoubleMuonLowMass5",
            "ParkingDoubleMuonLowMass6","ParkingDoubleMuonLowMass7"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               aod_to_disk=False,
               dqm_sequences=["@common", "@muon", "@heavyFlavor"],
               alca_producers=["TkAlJpsiMuMu", "TkAlUpsilonMuMu"],
               archival_node=None,
               scenario=ppScenario)

DATASETS = ["MuonShower"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False,
               write_aod=True,
               write_miniaod=True,
               write_nanoaod=True,
               physics_skims=["EXOCSCCluster"],
               scenario=ppScenario)

DATASETS = ["PPRefExotica"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False,
               write_aod=True,
               write_miniaod=True,
               write_nanoaod=True,
               physics_skims=["EXOCSCCluster"],
               scenario=ppScenario)

DATASETS = ["ParkingHH", "ParkingVBF0",
            "ParkingVBF1", "ParkingVBF2", "ParkingVBF3",
            "ParkingVBF4", "ParkingVBF5", "ParkingVBF6",
            "ParkingVBF7"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               aod_to_disk=False,
               dqm_sequences=["@common"],
               archival_node=None,
               scenario=ppScenario)
    
DATASETS = ["ParkingLLP"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               aod_to_disk=False,
               dqm_sequences=["@common", "@jetmet"],
               archival_node=None,
               scenario=ppScenario)
    
DATASETS = ["EmptyBX"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               scenario=ppScenario)

DATASETS = ["HighPtLowerPhotons", "HighPtPhoton30AndZ"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               scenario=ppScenario)

DATASETS = ["JetMET", "JetMET0", "JetMET1"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               alca_producers=["HcalCalIsoTrkProducerFilter", "TkAlJetHT", "HcalCalNoise"],
               dqm_sequences=["@common", "@jetmet", "@L1TMon", "@hcal"],
               physics_skims=["EXOHighMET", "EXODelayedJetMET", "JetHTJetPlusHOFilter", "EXODisappTrk", "LogError", "LogErrorMonitor"],
               timePerEvent=5.7,  # copied from JetHT - should be checked
               sizePerEvent=2250, # copied from JetHT - should be checked
               scenario=ppScenario)

DATASETS = ["PPRefHardProbes0", "PPRefHardProbes1", "PPRefHardProbes2"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               alca_producers=["HcalCalIsoTrkProducerFilter", "TkAlJetHT", "HcalCalNoise"],
               dqm_sequences=["@common", "@jetmet", "@L1TMon", "@hcal"],
               physics_skims=["EXOHighMET", "EXODelayedJetMET", "JetHTJetPlusHOFilter", "EXODisappTrk", "LogError", "LogErrorMonitor"],
               timePerEvent=5.7,
               sizePerEvent=2250,
               scenario=ppScenario)

DATASETS = ["JetHT"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
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
               write_dqm=True,
               alca_producers=["HcalCalNoise"],
               dqm_sequences=["@common", "@jetmet", "@L1TMon", "@hcal"],
               physics_skims=["EXOHighMET", "LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["MuonEG"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               physics_skims=["TopMuEG", "LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["Muon", "Muon0"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False,
               write_dqm=True,
               alca_producers=["TkAlMuonIsolated", "HcalCalIterativePhiSym", "MuAlCalIsolatedMu",
                               "HcalCalHO", "HcalCalHBHEMuonProducerFilter",
                               "SiPixelCalSingleMuonLoose", "SiPixelCalSingleMuonTight",
                               "TkAlZMuMu", "TkAlDiMuonAndVertex"],
               dqm_sequences=["@common", "@muon", "@lumi", "@L1TMuon", "@jetmet"],
               physics_skims=["ZMu", "EXODisappTrk", "LogError", "LogErrorMonitor", "EXOCSCCluster", "EXODisappMuon"],
               scenario=ppScenario)

DATASETS = ["Muon1"]
DATASETS += ["PPRefSingleMuon0", "PPRefSingleMuon1", "PPRefSingleMuon2"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False,
               write_dqm=True,
               alca_producers=["TkAlMuonIsolated", "HcalCalIterativePhiSym", "MuAlCalIsolatedMu",
                               "HcalCalHO", "HcalCalHBHEMuonProducerFilter",
                               "SiPixelCalSingleMuonLoose", "SiPixelCalSingleMuonTight",
                               "TkAlZMuMu", "TkAlDiMuonAndVertex"],
               dqm_sequences=["@common", "@muon", "@lumi", "@L1TMuon", "@jetmet"],
               physics_skims=["ZMu", "EXODisappTrk", "LogError", "LogErrorMonitor", "EXOCSCCluster", "EXODisappMuon"],
               scenario=ppScenario)

DATASETS = ["PPRefDoubleMuon0", "PPRefDoubleMuon1", "PPRefDoubleMuon2", "PPRefDoubleMuon3"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False,
               write_dqm=True,
               alca_producers=["TkAlZMuMu", "TkAlDiMuonAndVertex", "TkAlJpsiMuMu", "TkAlUpsilonMuMu"],
               dqm_sequences=["@common", "@muon", "@lumi", "@L1TMuon", "@jetmet"],
               physics_skims=["ZMu", "EXODisappTrk", "LogError", "LogErrorMonitor", "EXOCSCCluster", "EXODisappMuon"],
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


DATASETS = ["SingleMuon"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               alca_producers=["TkAlMuonIsolated", "HcalCalIterativePhiSym", "MuAlCalIsolatedMu",
                               "HcalCalHO", "HcalCalHBHEMuonProducerFilter",
                               "SiPixelCalSingleMuonLoose", "SiPixelCalSingleMuonTight"],
               dqm_sequences=["@common", "@muon", "@lumi", "@L1TMuon"],
               physics_skims=["ZMu", "LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["EGamma", "EGamma0", "EGamma1"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               alca_producers=["EcalUncalZElectron", "EcalUncalWElectron", "HcalCalIterativePhiSym",
                               "HcalCalIsoTrkProducerFilter", "EcalESAlign"],
               dqm_sequences=["@common", "@ecal", "@egamma", "@L1TEgamma"],
               physics_skims=["ZElectron","WElectron", "EXOMONOPOLE", "EXODisappTrk", "IsoPhotonEB", "LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["Tau"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               physics_skims=["EXODisappTrk", "LogError", "LogErrorMonitor"],
               scenario=ppScenario)

#############################################
### Standard Commisioning PDs (2022)      ###
#############################################

DATASETS = ["Commissioning"]

DATASETS += ["Commissioning1", "Commissioning2", "Commissioning3", "Commissioning4",
             "CommissioningMuons", "CommissioningEGamma", "CommissioningTaus", "CommissioningSingleJet", "CommissioningDoubleJet"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               alca_producers=["TkAlMinBias", "SiStripCalMinBias", "HcalCalIsoTrk"],
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

#############################################
### MiniDAQ                               ###
#############################################

DATASETS = ["MiniDaq"]
for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               raw_to_disk=True,
               dataset_lifetime=6*30*24*3600)

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
               write_reco=False, write_aod=False, write_miniaod=False, write_nanoaod=False, write_dqm=True,
               disk_node=None,
               tape_node=None,
               reco_split=alcarawSplitting,
               proc_version=alcarawProcVersion,
               alca_producers=["AlCaPCCZeroBias"],
               dqm_sequences=["@common"],
               timePerEvent=0.02,
               sizePerEvent=38,
               scenario=alcaLumiPixelsScenario)

DATASETS = ["AlCaLowPtJet"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               scenario=ppScenario)

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
               write_reco=False, write_aod=False, write_miniaod=False, write_nanoaod=False, write_dqm=False,
               tape_node=None,
               reco_split=alcarawSplitting,
               proc_version=alcarawProcVersion,
               alca_producers = [ "AlCaPCCZeroBias", "RawPCCProducer", "AlCaPCCRandom"],
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

DATASETS = ["AlCaLumiPixelsCountsUngated"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               write_reco=False, write_aod=False, write_miniaod=False, write_dqm=False,
               write_nanoaod=False,
               raw_to_disk=True,
               tape_node=None,
               reco_split=alcarawSplitting,
               proc_version=alcarawProcVersion,
               timePerEvent=0.02,
               sizePerEvent=38,
               scenario=alcaLumiPixelsScenario)

DATASETS = ["AlCaLumiPixelsCountsGated"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               write_reco=False, write_aod=False, write_miniaod=False, write_dqm=False,
               write_nanoaod=False,
               raw_to_disk=True,
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
            "HLTPhysics8", "HLTPhysics9", "HLTPhysics10",
            "HLTPhysics11", "HLTPhysics12", "HLTPhysics13",
            "HLTPhysics14", "HLTPhysics15", "HLTPhysics16",
            "HLTPhysics17", "HLTPhysics18", "HLTPhysics19"]

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

DATASETS = ["SpecialHLTPhysics", "SpecialHLTPhysics0", "SpecialHLTPhysics1",
            "SpecialHLTPhysics2", "SpecialHLTPhysics3", "SpecialHLTPhysics4",
            "SpecialHLTPhysics5", "SpecialHLTPhysics6", "SpecialHLTPhysics7",
            "SpecialHLTPhysics8", "SpecialHLTPhysics9", "SpecialHLTPhysics10",
            "SpecialHLTPhysics11", "SpecialHLTPhysics12", "SpecialHLTPhysics13",
            "SpecialHLTPhysics14", "SpecialHLTPhysics15", "SpecialHLTPhysics16",
            "SpecialHLTPhysics17", "SpecialHLTPhysics18", "SpecialHLTPhysics19",
            "SpecialHLTPhysics20", "SpecialHLTPhysics21", "SpecialHLTPhysics22",
            "SpecialHLTPhysics23", "SpecialHLTPhysics24", "SpecialHLTPhysics25",
            "SpecialHLTPhysics26", "SpecialHLTPhysics27", "SpecialHLTPhysics28",
            "SpecialHLTPhysics29", "SpecialHLTPhysics30", "SpecialHLTPhysics31"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               write_reco=False,
               write_dqm=True,
               write_miniaod=True,
               write_aod=True,
               dqm_sequences=["@common", "@ecal", "@jetmet", "@L1TMon", "@hcal", "@L1TEgamma"],
               alca_producers=["TkAlMinBias","LumiPixelsMinBias"],
               physics_skims=["LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["EphemeralHLTPhysics0","EphemeralHLTPhysics1", "EphemeralHLTPhysics2", "EphemeralHLTPhysics3",
            "EphemeralHLTPhysics4", "EphemeralHLTPhysics5", "EphemeralHLTPhysics6","EphemeralHLTPhysics7"
            "EphemeralHLTPhysics8", "EphemeralHLTPhysics9","EphemeralHLTPhysics10","EphemeralHLTPhysics11"
            "EphemeralHLTPhysics12","EphemeralHLTPhysics13","EphemeralHLTPhysics14","EphemeralHLTPhysics15"
            "EphemeralHLTPhysics16","EphemeralHLTPhysics17","EphemeralHLTPhysics18","EphemeralHLTPhysics19"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               dqm_sequences=["@none"],
               write_dqm=False,
               write_aod=False,
               archival_node=None,
               siteWhitelist = ["T2_CH_CERN_P5", "T2_CH_CERN"],
               scenario=ppScenario)

########################################################
### SpecialRandom PDs                                  ###
########################################################

DATASETS = ["SpecialRandom0", "SpecialRandom1", "SpecialRandom2",
            "SpecialRandom3", "SpecialRandom4", "SpecialRandom5",
            "SpecialRandom6", "SpecialRandom7", "SpecialRandom8",
            "SpecialRandom9", "SpecialRandom10", "SpecialRandom11",
            "SpecialRandom12", "SpecialRandom13", "SpecialRandom14",
            "SpecialRandom15", "SpecialRandom16", "SpecialRandom17",
            "SpecialRandom18", "SpecialRandom19", "SpecialRandom"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               write_reco=False,
               write_dqm=True,
               write_miniaod=True,
               write_aod=True,
               dqm_sequences=["@common", "@ecal", "@jetmet", "@L1TMon", "@hcal", "@L1TEgamma"],
               alca_producers=["TkAlMinBias","LumiPixelsMinBias"],
               physics_skims=["LogError", "LogErrorMonitor"],
               scenario=ppScenario)

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
               dqm_sequences=["@commonSiStripZeroBias", "@ecal", "@hcal", "@muon", "@jetmet"],
               timePerEvent=1,
               alca_producers=["SiStripCalZeroBias", "SiStripCalMinBias", "TkAlMinBias"],
               scenario=ppScenario)

########################################################
### ZeroBias PDs                                     ###
########################################################

DATASETS = ["ZeroBias", "ZeroBias0"]

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

DATASETS += ["ZeroBiasNonColliding"]

DATASETS += ["SpecialZeroBias", "SpecialZeroBias0", "SpecialZeroBias1", 
	     "SpecialZeroBias2", "SpecialZeroBias3", "SpecialZeroBias4", 
	     "SpecialZeroBias5", "SpecialZeroBias6", "SpecialZeroBias7",
	     "SpecialZeroBias8", "SpecialZeroBias9", "SpecialZeroBias10",
	     "SpecialZeroBias11", "SpecialZeroBias12", "SpecialZeroBias13",
	     "SpecialZeroBias14", "SpecialZeroBias15", "SpecialZeroBias16",
	     "SpecialZeroBias17", "SpecialZeroBias18", "SpecialZeroBias19"]

DATASETS += ["PPRefZeroBias0", "PPRefZeroBias1", "PPRefZeroBias2",
             "PPRefZeroBias3", "PPRefZeroBias4", "PPRefZeroBias5", "PPRefZeroBias6",
             "PPRefZeroBias7", "PPRefZeroBias8", "PPRefZeroBias9", "PPRefZeroBias10",
             "PPRefZeroBias11", "PPRefZeroBias12", "PPRefZeroBias13", "PPRefZeroBias14",
             "PPRefZeroBias15", "PPRefZeroBias16", "PPRefZeroBias17", "PPRefZeroBias18",
             "PPRefZeroBias19"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               write_reco=False,
               write_dqm=True,
               dqm_sequences=["@commonSiStripZeroBias", "@ecal", "@hcal", "@muon", "@jetmet", "@ctpps"],
               alca_producers=["SiStripCalZeroBias", "TkAlMinBias", "SiStripCalMinBias", "HcalCalIsolatedBunchSelector"],
               physics_skims=["LogError", "LogErrorMonitor"],
               timePerEvent=3.5,
               sizePerEvent=1500,
               scenario=ppScenario)

DATASETS = ["EphemeralZeroBias0", "EphemeralZeroBias1", "EphemeralZeroBias2", "EphemeralZeroBias3",
            "EphemeralZeroBias4", "EphemeralZeroBias5", "EphemeralZeroBias6", "EphemeralZeroBias7",
            "EphemeralZeroBias8", "EphemeralZeroBias9", "EphemeralZeroBias10", "EphemeralZeroBias11",
            "EphemeralZeroBias12", "EphemeralZeroBias13", "EphemeralZeroBias14", "EphemeralZeroBias15",
            "EphemeralZeroBias16", "EphemeralZeroBias17", "EphemeralZeroBias18", "EphemeralZeroBias19"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               dqm_sequences=["@none"],
               write_dqm=False,
               scenario=ppScenario)

########################################################
### Parking and Scouting PDs                         ###
########################################################

DATASETS = ["ScoutingPFRun3"]
for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               scenario=ppScenario)

DATASETS = ["ParkingDoubleElectronLowMass","ParkingDoubleElectronLowMass0"]
for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               archival_node=None,
               scenario=ppScenario)

DATASETS = ["ParkingDoubleElectronLowMass1","ParkingDoubleElectronLowMass2",
            "ParkingDoubleElectronLowMass3","ParkingDoubleElectronLowMass4","ParkingDoubleElectronLowMass5"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               aod_to_disk=False,
               siteWhitelist = ["T2_CH_CERN_P5", "T2_CH_CERN"],
               scenario=ppScenario)

DATASETS = ["RPCMonitor"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               scenario=ppScenario)

DATASETS = ["ScoutingMonitor"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               dqm_sequences=["@common"],
               write_reco=False, write_aod=False, write_miniaod=True, write_dqm=True,
               scenario=ppScenario)

DATASETS = ["ScoutingPFMonitor"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               dqm_sequences=["@common"],
               write_reco=False, write_aod=False, write_miniaod=True, write_dqm=True,
               scenario=ppScenario)

DATASETS = ["ScoutingCaloCommissioning", "ScoutingCaloHT", "ScoutingCaloMuon",
            "ScoutingPFCommissioning", "ScoutingPFHT", "ScoutingPFMuon"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               scenario=ppScenario)

DATASETS = ["AlCaElectron", "VRRandom", "VRRandom0", "VRRandom1", "VRRandom2", "VRRandom3",
             "VRRandom4", "VRRandom5", "VRRandom6", "VRRandom7", "VRRandom8", "VRRandom9",
             "VRRandom10", "VRRandom11", "VRRandom12", "VRRandom13", "VRRandom14", "VRRandom15",
             "VRZeroBias", "VirginRaw"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               scenario=ppScenario)

# PPS 2022
DATASETS = ["AlCaPPSPrompt"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False, write_aod=False, write_miniaod=False,
               write_nanoaod=False,
               write_dqm=True,
               alca_producers=["PPSCalMaxTracks"],
               dqm_sequences=["@none"],
               scenario=alcaPPSScenario)

#####################
### HI TESTS 2022 ###
#####################

DATASETS = ["HIHcalNZS"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=False,
               aod_to_disk=False,
               write_dqm=True,
               alca_producers=["HcalCalMinBias"],
               dqm_sequences=["@common", "@L1TMon", "@hcal"],
               scenario=HIhcalnzsScenario)

DATASETS = ["HIHLTPhysics"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=False,
               aod_to_disk=False,
               write_dqm=True,
               alca_producers=["TkAlMinBias"],
               dqm_sequences=["@common"],
               scenario=hiTestppScenario)

DATASETS = ["HIOnlineMonitor", "HITrackerNZS"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               aod_to_disk=False,
               raw_to_disk=False,
               scenario=hiTestppScenario)

DATASETS = ["HIEmptyBX"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               raw_to_disk=False,
               aod_to_disk=False,
               dqm_sequences=["@common"],
               scenario=hiTestppScenario)

DATASETS = ["HITestRaw0", "HITestRaw1", "HITestRaw2", "HITestRaw3", "HITestRaw4", "HITestRaw5",
            "HITestRaw6", "HITestRaw7", "HITestRaw8", "HITestRaw9", "HITestRaw10", "HITestRaw11",
            "HITestRaw12", "HITestRaw13", "HITestRaw14", "HITestRaw15", "HITestRaw16", "HITestRaw17",
            "HITestRaw18", "HITestRaw19", "HITestRaw20", "HITestRaw21", "HITestRaw22", "HITestRaw23"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=False,
               aod_to_disk=False,
               write_dqm=True,
               alca_producers=["SiStripCalZeroBias", "SiStripCalMinBias","TkAlMinBias",
                               "HcalCalIsolatedBunchSelector", "HcalCalIterativePhiSym","HcalCalMinBias",
                               "TkAlJpsiMuMu", "TkAlUpsilonMuMu","TkAlZMuMu","TkAlMuonIsolated"],
               dqm_sequences=["@commonSiStripZeroBias", "@ecal", "@hcal", "@muon", "@jetmet"],
               scenario=hiTestppScenario)
DATASETS = ["HIForward0", "HIForward1", "HIForward2",
	    "HIForward3", "HIForward4", "HIForward5",
            "HIForward6", "HIForward7", "HIForward8",
            "HIForward9", "HIForward10", "HIForward11",
            "HIForward12", "HIForward13", "HIForward14",
            "HIForward15", "HIForward16", "HIForward17",
            "HIForward18", "HIForward19"]
for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               timePerEvent=1,
               raw_to_disk=False,
               aod_to_disk=True,
               write_dqm=True,
               alca_producers=["EcalUncalZElectron", "EcalUncalWElectron", "EcalESAlign", "MuAlCalIsolatedMu", 
                               "TkAlDiMuonAndVertex", "HcalCalHO", "HcalCalIsoTrkProducerFilter", "HcalCalHBHEMuonProducerFilter",
                               "SiStripCalZeroBias", "SiStripCalMinBias","TkAlMinBias",
                               "HcalCalIsolatedBunchSelector", "HcalCalIterativePhiSym","HcalCalMinBias",
                               "TkAlJpsiMuMu", "TkAlUpsilonMuMu","TkAlZMuMu","TkAlMuonIsolated"],
               dqm_sequences=["@commonSiStripZeroBias", "@ecal", "@hcal", "@muon", "@jetmet", "@egamma"],
               scenario=hiForwardScenario)
    
DATASETS = ["HIMinimumBias0", "HIMinimumBias1", "HIMinimumBias2", "HIMinimumBias3", 
            "HIMinimumBias4", "HIMinimumBias5", "HIMinimumBias6", "HIMinimumBias7",
            "HIMinimumBias8", "HIMinimumBias9", "HIMinimumBias10", "HIMinimumBias11",
            "HIMinimumBias12", "HIMinimumBias13", "HIMinimumBias14", "HIMinimumBias15",
            "HIMinimumBias16", "HIMinimumBias17", "HIMinimumBias18", "HIMinimumBias19"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=False,
               write_dqm=True,
               alca_producers=["SiStripCalZeroBias", "SiStripCalMinBias", "TkAlMinBias"],
               dqm_sequences=["@commonSiStripZeroBias"],
               scenario=hiTestppScenario)

DATASETS = ["HIEphemeralHLTPhysics"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=False,
               write_dqm=True,
               disk_node="T2_US_Vanderbilt",
               dqm_sequences=["@commonSiStripZeroBias"],
               scenario=hiTestppScenario)

DATASETS = ["HIEphemeralZeroBias0", "HIEphemeralZeroBias1"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=False,
               write_dqm=True,
               timePerEvent=1,
               disk_node="T2_US_Vanderbilt",
               dqm_sequences=["@commonSiStripZeroBias"],
               scenario=hiTestppScenario)

DATASETS = ["HITestRawPrime0", "HITestRawPrime1", "HITestRawPrime2", "HITestRawPrime3", "HITestRawPrime4",
            "HITestRawPrime5", "HITestRawPrime6", "HITestRawPrime7", "HITestRawPrime8", "HITestRawPrime9",
            "HITestRawPrime10", "HITestRawPrime11", "HITestRawPrime12", "HITestRawPrime13", "HITestRawPrime14",
            "HITestRawPrime15", "HITestRawPrime16", "HITestRawPrime17", "HITestRawPrime18", "HITestRawPrime19",
            "HITestRawPrime20", "HITestRawPrime21", "HITestRawPrime22", "HITestRawPrime23"]

DATASETS += ["HIPhysicsRawPrime0", "HIPhysicsRawPrime1"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=False,
               aod_to_disk=True,
               write_dqm=True,
               timePerEvent=3,
               siteWhitelist = ["T2_CH_CERN"],
               maxMemoryperCore=2500,
               disk_node="T2_US_Vanderbilt",
               alca_producers=["EcalUncalZElectron", "EcalUncalWElectron", "EcalESAlign", "MuAlCalIsolatedMu", 
                               "TkAlDiMuonAndVertex", "HcalCalHO", "HcalCalIsoTrkProducerFilter", "HcalCalHBHEMuonProducerFilter",
                               "SiStripCalZeroBias", "SiStripCalMinBias","TkAlMinBias",
                               "HcalCalIsolatedBunchSelector", "HcalCalIterativePhiSym","HcalCalMinBias",
                               "TkAlJpsiMuMu", "TkAlUpsilonMuMu","TkAlZMuMu","TkAlMuonIsolated"],
               dqm_sequences=["@commonSiStripZeroBias", "@ecal", "@hcal", "@muon", "@jetmet", "@egamma"],
               physics_skims=["PbPbEMu", "PbPbZEE", "PbPbZMM", "LogError", "LogErrorMonitor"],
               scenario=hiRawPrimeScenario)

DATASETS = ["HIPhysicsRawPrime2", "HIPhysicsRawPrime3", "HIPhysicsRawPrime4",
            "HIPhysicsRawPrime5", "HIPhysicsRawPrime6", "HIPhysicsRawPrime7", "HIPhysicsRawPrime8", "HIPhysicsRawPrime9",
            "HIPhysicsRawPrime10", "HIPhysicsRawPrime11", "HIPhysicsRawPrime12", "HIPhysicsRawPrime13", "HIPhysicsRawPrime14",
            "HIPhysicsRawPrime15", "HIPhysicsRawPrime16", "HIPhysicsRawPrime17", "HIPhysicsRawPrime18", "HIPhysicsRawPrime19",
            "HIPhysicsRawPrime20", "HIPhysicsRawPrime21", "HIPhysicsRawPrime22", "HIPhysicsRawPrime23", "HIPhysicsRawPrime24",
            "HIPhysicsRawPrime25", "HIPhysicsRawPrime26", "HIPhysicsRawPrime27", "HIPhysicsRawPrime28", "HIPhysicsRawPrime29",
            "HIPhysicsRawPrime30", "HIPhysicsRawPrime31"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=False,
               aod_to_disk=False,
               write_dqm=False,
               timePerEvent=3,
               alca_producers=["EcalUncalZElectron", "EcalUncalWElectron", "EcalESAlign", "MuAlCalIsolatedMu", 
                               "TkAlDiMuonAndVertex", "HcalCalHO", "HcalCalIsoTrkProducerFilter", "HcalCalHBHEMuonProducerFilter",
                               "SiStripCalZeroBias", "SiStripCalMinBias","TkAlMinBias",
                               "HcalCalIsolatedBunchSelector", "HcalCalIterativePhiSym","HcalCalMinBias",
                               "TkAlJpsiMuMu", "TkAlUpsilonMuMu","TkAlZMuMu","TkAlMuonIsolated"],
               dqm_sequences=["@none"],
               physics_skims=["PbPbEMu", "PbPbZEE", "PbPbZMM", "LogError", "LogErrorMonitor"],
               scenario=hiRawPrimeScenario)

DATASETS = ["HIZeroBias0", "HIZeroBias1", "HIZeroBias2"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               raw_to_disk=False,
               aod_to_disk=True,
               dqm_sequences=["@commonSiStripZeroBias", "@ecal", "@hcal", "@muon", "@jetmet", "@egamma"],
               alca_producers=["SiStripCalZeroBias", "TkAlMinBias", "SiStripCalMinBias"],
               timePerEvent=1,
               scenario=hiForwardScenario)

#######################
### ignored streams ###
#######################
#specifyStreams(tier0Config, ["HIForward0", "HIForward1", "HIForward2",
#            "HIForward3", "HIForward4", "HIForward5",
#            "HIForward6", "HIForward7", "HIForward8",
#            "HIForward9", "HIForward10", "HIForward11",
#            "HIForward12", "HIForward13", "HIForward14",
#            "HIForward15", "HIForward16", "HIForward17",
#            "HIForward18", "HIForward19"])

ignoreStream(tier0Config, "Error")
ignoreStream(tier0Config, "HLTMON")
ignoreStream(tier0Config, "EventDisplay")
ignoreStream(tier0Config, "HIEventDisplay")
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
