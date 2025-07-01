"""
_OfflineConfiguration_
Processing configuration for the Tier0 - Replay version
"""
from __future__ import print_function

from T0.RunConfig.Tier0Config import addDataset
from T0.RunConfig.Tier0Config import createTier0Config
from T0.RunConfig.Tier0Config import setAcquisitionEra
from T0.RunConfig.Tier0Config import setEmulationAcquisitionEra
from T0.RunConfig.Tier0Config import setDefaultScramArch
from T0.RunConfig.Tier0Config import setScramArch
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
from T0.RunConfig.Tier0Config import setInjectLimit
from T0.RunConfig.Tier0Config import setStreamerPNN
from T0.RunConfig.Tier0Config import setEnableUniqueWorkflowName
from T0.RunConfig.Tier0Config import addSiteConfig
from T0.RunConfig.Tier0Config import setStorageSite
from T0.RunConfig.Tier0Config import setExtraStreamDatasetMap
from T0.RunConfig.Tier0Config import setHelperAgentStreams

# Create the Tier0 configuration object
tier0Config = createTier0Config()

# Set the verstion configuration (not used at the moment)
setConfigVersion(tier0Config, "replace with real version")
specifyStreams(tier0Config, [
    "PhysicsIonPhysics0", "PhysicsIonPhysics1", "PhysicsIonPhysics2", "PhysicsIonPhysics3", "PhysicsIonPhysics4",
    "PhysicsIonPhysics5", "PhysicsIonPhysics6", "PhysicsIonPhysics7", "PhysicsIonPhysics8", "PhysicsIonPhysics9",
    "PhysicsIonPhysics10", "PhysicsIonPhysics11", "PhysicsIonPhysics12", "PhysicsIonPhysics13", "PhysicsIonPhysics14",
    "PhysicsIonPhysics15", "PhysicsIonPhysics16", "PhysicsIonPhysics17", "PhysicsIonPhysics18", "PhysicsIonPhysics19",
    "PhysicsIonPhysics20", "PhysicsIonPhysics21", "PhysicsIonPhysics22", "PhysicsIonPhysics23", "PhysicsIonPhysics24",
    "PhysicsIonPhysics25", "PhysicsIonPhysics26", "PhysicsIonPhysics27", "PhysicsIonPhysics28", "PhysicsIonPhysics29",
    "PhysicsIonPhysics30", "PhysicsIonPhysics31", "PhysicsIonPhysics32", "PhysicsIonPhysics33", "PhysicsIonPhysics34",
    "PhysicsIonPhysics35", "PhysicsIonPhysics36", "PhysicsIonPhysics37", "PhysicsIonPhysics38", "PhysicsIonPhysics39",
    "PhysicsIonPhysics40", "PhysicsIonPhysics41", "PhysicsIonPhysics42", "PhysicsIonPhysics43", "PhysicsIonPhysics44",
    "PhysicsIonPhysics45", "PhysicsIonPhysics46", "PhysicsIonPhysics47", "PhysicsIonPhysics48", "PhysicsIonPhysics49",
    "PhysicsIonPhysics50", "PhysicsIonPhysics51", "PhysicsIonPhysics52", "PhysicsIonPhysics53", "PhysicsIonPhysics54",
    "PhysicsIonPhysics55", "PhysicsIonPhysics56", "PhysicsIonPhysics57", "PhysicsIonPhysics58", "PhysicsIonPhysics59"
])

# Set run number to replay
# 382686 - Collisions, 43.3 pb-1, 23.9583 TB NEW
# 386674  Cosmics ~40 minutes in Run2024I with occupancy issues

setInjectRuns(tier0Config, [393952]) # 386925: 2024 Collisions, 390094: 2025 Cosmics, 390951: 2025 900 GeV Collisions

# Use this in order to limit the number of lumisections to process
#setInjectLimit(tier0Config, 10)
setInjectLimit(tier0Config, 50)
# Settings up sites
processingSite = "T2_CH_CERN"
storageSite = "T0_CH_CERN_Disk"
streamerPNN = "T0_CH_CERN_Disk"

addSiteConfig(tier0Config, "T0_CH_CERN_Disk",
                siteLocalConfig="/cvmfs/cms.cern.ch/SITECONF/T0_CH_CERN/JobConfig/site-local-config.xml",
                overrideCatalog="T2_CH_CERN,,T0_CH_CERN,CERN_EOS_T0,XRootD",
                siteLocalRucioConfig="/cvmfs/cms.cern.ch/SITECONF/T0_CH_CERN/storage.json",
                )

addSiteConfig(tier0Config, "EOS_PILOT",
                siteLocalConfig="/cvmfs/cms.cern.ch/SITECONF/T0_CH_CERN/JobConfig/site-local-config_EOS_PILOT.xml",
                overrideCatalog="trivialcatalog_file:/cvmfs/cms.cern.ch/SITECONF/T0_CH_CERN/PhEDEx/storage_EOS_PILOT.xml?protocol=eos"
                )

### Settings up sites for eos pilot

#processingSite = "T2_CH_CERN"
#storageSite = "T0_CH_CERN_Pilot"
#streamerPNN = "T0_CH_CERN_Pilot"
#addSiteConfig(tier0Config, "T0_CH_CERN_Pilot",
#                siteLocalConfig="/cvmfs/cms.cern.ch/SITECONF/T0_CH_CERN/JobConfig/site-local-config_EOS_PILOT.xml",
#                overrideCatalog="T2_CH_CERN,,T0_CH_CERN,EOS_PILOT,XRootD",
#                siteLocalRucioConfig="/cvmfs/cms.cern.ch/SITECONF/T0_CH_CERN/storage.json",
#                )


# Set global parameters:
#  Acquisition era
#  BaseRequestPriority
#  Backfill mode
#  Data type
#  Processing site (where jobs run)
#  PhEDEx locations
setAcquisitionEra(tier0Config, "Tier0_OXYREPLAY_2025")
setEmulationAcquisitionEra(tier0Config, "Emulation2025", repack=False)
setBaseRequestPriority(tier0Config, 260000)
setBackfill(tier0Config, 1)
setBulkDataType(tier0Config, "data")
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
setDQMUploadUrl(tier0Config, "https://cmsweb.cern.ch/dqm/dev")

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
    'default': "CMSSW_15_0_9_patch3"
}

# Configure ScramArch
setDefaultScramArch(tier0Config, "el8_amd64_gcc12")
setScramArch(tier0Config, "CMSSW_12_4_9", "el8_amd64_gcc10")
setScramArch(tier0Config, "CMSSW_12_3_0", "cs8_amd64_gcc10")
setScramArch(tier0Config, "CMSSW_13_0_9", "el8_amd64_gcc11")

# Configure scenarios
ppScenario = "ppEra_Run3_2025"
ppRefScenario = "ppEra_Run3_2024_ppRef"
ppScenarioB0T = "ppEra_Run3"
cosmicsScenario = "cosmicsEra_Run3"
hcalnzsScenario = "hcalnzsEra_Run3"
alcaTrackingOnlyScenario = "trackingOnlyEra_Run3"
alcaTestEnableScenario = "AlCaTestEnable"
alcaLumiPixelsScenario = "AlCaLumiPixels_Run3"
alcaPPSScenario = "AlCaPPS_Run3"
hiTestppScenario = "ppEra_Run3_pp_on_PbPb_2023"
hiRawPrimeScenario = "ppEra_Run3_pp_on_PbPb_approxSiStripClusters_2023"
hltScoutingScenario = "hltScoutingEra_Run3_2025"
AlCaHcalIsoTrkScenario = "AlCaHcalIsoTrk_Run3"
OXYScenario = "ppEra_Run3_2025_OXY"


# Procesing version number replays
# Taking Replay processing ID from the last 8 digits of the DeploymentID
dt = int(open("/data/tier0/DeploymentID.txt","r").read()[4:])
defaultProcVersion = dt
expressProcVersion = dt
alcarawProcVersion = dt

# Defaults for GlobalTag


expressGlobalTag = "150X_dataRun3_Express_v2"
promptrecoGlobalTag = "150X_dataRun3_Prompt_v1"
repackGlobalTag = "150X_dataRun3_Prompt_v1_ParkingDoubleMuonLowMass_v2"

# Mandatory for CondDBv2
globalTagConnect = "frontier://PromptProd/CMS_CONDITIONS"

# Multicore settings
numberOfCores = 8

# Splitting parameters for PromptReco
defaultRecoSplitting = 750 * numberOfCores
hiRecoSplitting = 200 * numberOfCores
alcarawSplitting = 20000 * numberOfCores

# Replay Dataset lifetime
replayDatasetLifetime = 7*24*3600

#
# Setup repack and express mappings
#
repackVersionOverride = {
}

expressVersionOverride = {
}

# Additional Stream-Dataset mapping
setExtraStreamDatasetMap(tier0Config,{
                                        "L1Scouting": {"Dataset":"L1Scouting"},
                                        "L1ScoutingSelection": {"Dataset":"L1ScoutingSelection"}
                                    }
                         )

#set default repack settings for bulk streams
addRepackConfig(tier0Config, "Default",
                proc_ver=defaultProcVersion,
                global_tag=repackGlobalTag,
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

# Stream PhysicsScoutingPFMonitor --> PD ScoutingPFMonitor --> Repacked to RAW
# Stream ScoutingPF --> PD ScoutingPF_Run3 --> Repacked to HLTSCOUT
addRepackConfig(tier0Config, "ScoutingPF",
                proc_ver=defaultProcVersion,
                dataTier="HLTSCOUT",
                versionOverride=repackVersionOverride)

addRepackConfig(tier0Config, "L1ScoutingSelection",
                proc_ver=defaultProcVersion,
                dataTier="L1SCOUT",
                versionOverride=repackVersionOverride)

addRepackConfig(tier0Config, "L1Scouting",
                proc_ver=defaultProcVersion,
                dataTier="L1SCOUT",
                versionOverride=repackVersionOverride)

addDataset(tier0Config, "Default",
           do_reco=False,
           write_reco=False, write_aod=True, write_miniaod=True, write_nanoaod=True, write_dqm=False,
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
           nano_flavours=['@PHYS', '@L1'],
           blockCloseDelay=1200,
           timePerEvent=5,
           sizePerEvent=1500,
           maxMemoryperCore=2000,
           dataset_lifetime=replayDatasetLifetime,#lifetime for container rules. Default 14 days
           scenario=OXYScenario)

#############################
### Express configuration ###
#############################

addExpressConfig(tier0Config, "Express",
                 scenario=OXYScenario,
                 diskNode="T0_CH_CERN_Disk",
                 data_tiers=["FEVT"],
                 write_dqm=True,
                 alca_producers=["SiStripPCLHistos", "SiStripCalZeroBias", "SiStripCalMinBias", "SiStripCalMinBiasAAG",
                                 "TkAlMinBias", "SiPixelCalZeroBias", "SiPixelCalSingleMuon", "SiPixelCalSingleMuonTight",
                                 "TkAlZMuMu",
                                 "PromptCalibProd", "PromptCalibProdSiStrip", "PromptCalibProdSiPixelAli",
                                 "PromptCalibProdSiStripGains", "PromptCalibProdSiStripGainsAAG", "PromptCalibProdSiPixel",
                                 "PromptCalibProdSiPixelLA", "PromptCalibProdSiStripHitEff", "PromptCalibProdSiPixelAliHG",
                                 "PromptCalibProdSiPixelAliHGComb"
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
                 dataset_lifetime=7*24*3600,#lifetime for container rules. Default 14 days
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
                 dataset_lifetime=replayDatasetLifetime,#lifetime for container rules. Default 14 days
                 versionOverride=expressVersionOverride)

addExpressConfig(tier0Config, "HLTMonitor",
                 scenario=OXYScenario,
                 diskNode="T0_CH_CERN_Disk",
                 data_tiers=["FEVTHLTALL"],
                 write_dqm=True,
                 alca_producers=["TkAlHLTTracks", "TkAlHLTTracksZMuMu", "PromptCalibProdSiPixelAliHLTHGC"],
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
                 dataset_lifetime=replayDatasetLifetime,#lifetime for container rules. Default 14 days
                 versionOverride=expressVersionOverride)

addExpressConfig(tier0Config, "CosmicHLTMonitor",
                 scenario=cosmicsScenario,
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
                 dataset_lifetime=replayDatasetLifetime,#lifetime for container rules. Default 14 days
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
                 dataType="data",
                 dataset_lifetime=replayDatasetLifetime,#lifetime for container rules. Default 14 days
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
                 dataset_lifetime=replayDatasetLifetime,#lifetime for container rules. Default 14 days
                 diskNode="T0_CH_CERN_Disk")

addExpressConfig(tier0Config, "ALCALumiPixelsCountsExpress",
                 scenario=alcaLumiPixelsScenario,
                 data_tiers=["ALCARECO"],
                 write_dqm=True,
                 alca_producers=["AlCaPCCRandom", "PromptCalibProdLumiPCC"],
                 dqm_sequences=[],
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
                 dataset_lifetime=replayDatasetLifetime,#lifetime for container rules. Default 14 days
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
                 dataset_lifetime=replayDatasetLifetime,#lifetime for container rules. Default 14 days
                 diskNode="T0_CH_CERN_Disk",
                 versionOverride=expressVersionOverride)

###################################
### Special Runs Express PDs    ###
###################################

addExpressConfig(tier0Config, "SpecialRunExpressStream",
                 scenario=OXYScenario,
                 diskNode="T0_CH_CERN_Disk",
                 data_tiers=[], # --> FEVT, RAW, ALCARECO... ?
                 write_dqm=True,
                 alca_producers=[],
                 dqm_sequences=[],
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
                 dataset_lifetime=7*24*3600,#lifetime for container rules. Default 14 days
                 versionOverride=expressVersionOverride)

#####################
### HI Tests 2018 ###
#####################

addExpressConfig(tier0Config, "HIExpress",
                 scenario=hiTestppScenario,
                 diskNode="T0_CH_CERN_Disk",
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
                 dataset_lifetime=replayDatasetLifetime,#lifetime for container rules. Default 14 days
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
                 dataset_lifetime=replayDatasetLifetime,#lifetime for container rules. Default 14 days
                 diskNode="T0_CH_CERN_Disk")
                 
###################################
### Special Runs Express PDs    ###
###################################

addExpressConfig(tier0Config, "SpecialRunExpressStream",
                 scenario=OXYScenario,
                 diskNode="T0_CH_CERN_Disk",
                 data_tiers=[], # --> FEVT, RAW, ALCARECO... ?
                 write_dqm=True,
                 alca_producers=[],
                 dqm_sequences=[],
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
                 dataset_lifetime=7*24*3600,#lifetime for container rules. Default 14 days
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
               scenario=OXYScenario)

DATASETS = ["Cosmics"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False,
               write_aod=True,
               write_miniaod=False,
               write_nanoaod=False,
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
               scenario=OXYScenario)

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
               scenario=OXYScenario)

DATASETS = ["ReservedDoubleMuonLowMass"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               scenario=OXYScenario)

DATASETS = ["ParkingSingleMuon0","ParkingSingleMuon1","ParkingSingleMuon2","ParkingSingleMuon3",
            "ParkingSingleMuon4","ParkingSingleMuon5","ParkingSingleMuon6",
            "ParkingSingleMuon7","ParkingSingleMuon8","ParkingSingleMuon9",
            "ParkingSingleMuon10","ParkingSingleMuon11", "ParkingSingleMuon12",
            "ParkingSingleMuon13","ParkingSingleMuon14","ParkingSingleMuon15"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               scenario=OXYScenario)


DATASETS = ["ParkingAnomalyDetection"]
for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               aod_to_disk=False,
               archival_node=None,
               tape_node=None,
               scenario=OXYScenario)
    
DATASETS = ["ParkingDoubleMuonLowMass0","ParkingDoubleMuonLowMass1","ParkingDoubleMuonLowMass2",
            "ParkingDoubleMuonLowMass3"]
    
for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common", "@muon", "@heavyFlavor"],
               alca_producers=["TkAlJpsiMuMu", "TkAlUpsilonMuMu"],
               nano_flavours=["@PHYS", "@L1", "@BPH"],
               tape_node=None,
               scenario=OXYScenario)

DATASETS = ["ParkingDoubleMuonLowMass4","ParkingDoubleMuonLowMass5",
            "ParkingDoubleMuonLowMass6","ParkingDoubleMuonLowMass7"]
    
for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common", "@muon", "@heavyFlavor"],
               alca_producers=["TkAlJpsiMuMu", "TkAlUpsilonMuMu"],
               nano_flavours=["@PHYS", "@L1", "@BPH"],
               scenario=OXYScenario)
    
DATASETS = ["EmittanceScan0", "EmittanceScan1", "EmittanceScan2", 
            "EmittanceScan3", "EmittanceScan4", "EmittanceScan5"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               aod_to_disk=False,
               archival_node=None,
               tape_node=None,
               scenario=OXYScenario)
    
DATASETS = ["MuonShower"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False,
               write_aod=True,
               write_miniaod=True,
               write_nanoaod=True,
               physics_skims=["EXOCSCCluster"],
               scenario=OXYScenario)

DATASETS = ["ParkingLLP0", "ParkingLLP1"]
for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               aod_to_disk=False,
               dqm_sequences=["@common", "@jetmet"],
               physics_skims=["EXODelayedJet", "EXODTCluster", "EXOLLPJetHCAL"],
               scenario=OXYScenario)

DATASETS = ["ParkingHH0", "ParkingHH1", "ParkingVBF0",
            "ParkingVBF1", "ParkingVBF2", "ParkingVBF3",
            "ParkingVBF4", "ParkingVBF5", "ParkingVBF6",
            "ParkingVBF7"]
for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               aod_to_disk=False,
               dqm_sequences=["@common"],
               scenario=OXYScenario)

DATASETS = ["EmptyBX"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               scenario=OXYScenario)

DATASETS = ["HighPtLowerPhotons", "HighPtPhoton30AndZ"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               scenario=OXYScenario)

DATASETS = ["JetMET0", "JetMET1"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               alca_producers=["TkAlJetHT", "HcalCalNoise"],
               dqm_sequences=["@common", "@jetmet", "@L1TMon", "@hcal"],
               physics_skims=["EXOHighMET", "EXODelayedJetMET", "JetHTJetPlusHOFilter", "EXODisappTrk", "EXOSoftDisplacedVertices", "TeVJet", "LogError", "LogErrorMonitor", "EXOMONOPOLE", "EXODisplacedJet"],
               timePerEvent=5.7,  # copied from JetHT - should be checked
               sizePerEvent=2250, # copied from JetHT - should be checked
               scenario=OXYScenario)

DATASETS = ["PPRefHardProbes0", "PPRefHardProbes1", "PPRefHardProbes2", "PPRefHardProbes3", "PPRefHardProbes4"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               alca_producers=["HcalCalIsoTrkProducerFilter", "TkAlJetHT", "HcalCalNoise"],
               dqm_sequences=["@common", "@jetmet", "@L1TMon", "@hcal"],
               physics_skims=["EXOHighMET", "EXODelayedJetMET", "JetHTJetPlusHOFilter", "EXODisappTrk", "LogError", "LogErrorMonitor"],
               timePerEvent=5.7,
               sizePerEvent=2250,
               scenario=ppRefScenario)

DATASETS = ["MuonEG"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               physics_skims=["TopMuEG", "LogError", "LogErrorMonitor"],
               scenario=OXYScenario)

DATASETS = ["Muon0", "Muon1"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               alca_producers=["TkAlMuonIsolated", "HcalCalIterativePhiSym", "MuAlCalIsolatedMu",
                               "HcalCalHO", "HcalCalHBHEMuonProducerFilter",
                               "SiPixelCalSingleMuonLoose", "SiPixelCalSingleMuonTight",
                               "TkAlZMuMu", "TkAlDiMuonAndVertex"],
               dqm_sequences=["@common", "@muon", "@lumi", "@L1TMuon", "@jetmet"],
               physics_skims=["MUOJME", "ZMu", "EXODisappTrk", "EXOCSCCluster", "EXODisappMuon", "LogError", "LogErrorMonitor"],
               scenario=OXYScenario)

DATASETS = ["PPRefSingleMuon0", "PPRefSingleMuon1", "PPRefSingleMuon2", "PPRefSingleMuon3"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               alca_producers=["TkAlMuonIsolated", "HcalCalIterativePhiSym", "MuAlCalIsolatedMu",
                               "HcalCalHO", "HcalCalHBHEMuonProducerFilter",
                               "SiPixelCalSingleMuonLoose", "SiPixelCalSingleMuonTight",
                               "TkAlZMuMu", "TkAlDiMuonAndVertex"],
               dqm_sequences=["@common", "@muon", "@lumi", "@L1TMuon", "@jetmet"],
               physics_skims=["ZMu", "EXODisappTrk", "LogError", "LogErrorMonitor", "EXOCSCCluster", "EXODisappMuon"],
               scenario=ppRefScenario)

DATASETS = ["PPRefDoubleMuon0", "PPRefDoubleMuon1", "PPRefDoubleMuon2", "PPRefDoubleMuon3"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False,
               write_dqm=True,
               alca_producers=["TkAlZMuMu", "TkAlDiMuonAndVertex", "TkAlJpsiMuMu", "TkAlUpsilonMuMu"],
               dqm_sequences=["@common", "@muon", "@lumi", "@L1TMuon", "@jetmet"],
               physics_skims=["ZMu", "EXODisappTrk", "LogError", "LogErrorMonitor", "EXOCSCCluster", "EXODisappMuon"],
               scenario=ppRefScenario)

DATASETS = ["NoBPTX"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=False,
               write_dqm=True,
               alca_producers=["TkAlCosmicsInCollisions"],
               dqm_sequences=["@common"],
               physics_skims=["EXONoBPTXSkim", "LogError", "LogErrorMonitor"],
               scenario=OXYScenario)

DATASETS = ["EGamma0", "EGamma1", "EGamma2", "EGamma3"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               alca_producers=["EcalUncalZElectron", "EcalUncalWElectron", "HcalCalIterativePhiSym",
                               "HcalCalIsoTrkProducerFilter", "EcalESAlign"],
               dqm_sequences=["@common", "@ecal", "@egamma", "@L1TEgamma"],
               physics_skims=["ZElectron","WElectron", "EGMJME", "EXOMONOPOLE", "EXODisappTrk", "IsoPhotonEB", "LogError", "LogErrorMonitor"],
               scenario=OXYScenario)

DATASETS = ["Tau"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               dqm_sequences=["@common"],
               physics_skims=["EXODisappTrk", "LogError", "LogErrorMonitor"],
               scenario=OXYScenario)

#############################################
### Standard Commisioning PDs (2022)      ###
#############################################

DATASETS = ["Commissioning"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               alca_producers=["TkAlMinBias", "SiStripCalMinBias"],
               dqm_sequences=["@common", "@L1TMon", "@hcal"],
               physics_skims=["EcalActivity", "LogError", "LogErrorMonitor"],
               timePerEvent=12,
               sizePerEvent=4000,
               scenario=OXYScenario)

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
               scenario=OXYScenario)

DATASETS = ["L1Accept", "L1Accepts"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               write_dqm=False,
               write_aod=True,
               write_miniaod=True,
               write_reco=False,
               dqm_sequences=["@common"],
               scenario=OXYScenario)

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
               scenario=OXYScenario)

########################################################
### Pilot Tests PDs                                  ###
########################################################
DATASETS = ["AlCaLumiPixelsCountsPrompt0", "AlCaLumiPixelsCountsPrompt1", "AlCaLumiPixelsCountsPrompt2", "AlCaLumiPixelsCountsPrompt3",
            "AlCaLumiPixelsCountsPrompt4", "AlCaLumiPixelsCountsPrompt5", "AlCaLumiPixelsCountsPrompt6", "AlCaLumiPixelsCountsPrompt7",
            "AlCaLumiPixelsCountsPrompt8", "AlCaLumiPixelsCountsPrompt9", "AlCaLumiPixelsCountsPrompt10", "AlCaLumiPixelsCountsPrompt11",
            "AlCaLumiPixelsCountsPrompt12", "AlCaLumiPixelsCountsPrompt",
	    "AlCaLumiPixelsCountsPromptHighRate0", "AlCaLumiPixelsCountsPromptHighRate1", "AlCaLumiPixelsCountsPromptHighRate2", 
	    "AlCaLumiPixelsCountsPromptHighRate3", "AlCaLumiPixelsCountsPromptHighRate4", "AlCaLumiPixelsCountsPromptHighRate5"]

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
               write_nanoaod=False,
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
               disk_node=None,
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
               alca_producers=["EcalCalPhiSym"],
               scenario=OXYScenario)

DATASETS = ["AlCaP0"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               alca_producers=["EcalCalPi0Calib", "EcalCalEtaCalib"],
               scenario=OXYScenario)

DATASETS = ["AlCaHcalIsoTrk"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               alca_producers=["HcalCalIsoTrkFromAlCaRaw"],
               scenario=AlCaHcalIsoTrkScenario)
    
########################################################
### HLTPhysics PDs                                   ###
########################################################

DATASETS = ["HLTPhysics"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               write_reco=False,
               write_dqm=True,
               write_miniaod=True,
               write_aod=True,
               dqm_sequences=["@common", "@ecal", "@jetmet", "@L1TMon", "@hcal", "@L1TEgamma"],
               alca_producers=["TkAlMinBias", "TkAlV0s"],
               physics_skims=["LogError", "LogErrorMonitor"],
               scenario=OXYScenario)

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
               scenario=OXYScenario)

DATASETS = ["EphemeralHLTPhysics0","EphemeralHLTPhysics1", "EphemeralHLTPhysics2", "EphemeralHLTPhysics3",
            "EphemeralHLTPhysics4", "EphemeralHLTPhysics5", "EphemeralHLTPhysics6","EphemeralHLTPhysics7",
            "EphemeralHLTPhysics8", "EphemeralHLTPhysics9","EphemeralHLTPhysics10","EphemeralHLTPhysics11",
            "EphemeralHLTPhysics12","EphemeralHLTPhysics13","EphemeralHLTPhysics14","EphemeralHLTPhysics15",
            "EphemeralHLTPhysics16","EphemeralHLTPhysics17","EphemeralHLTPhysics18","EphemeralHLTPhysics19"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               dqm_sequences=["@none"],
               write_dqm=False,
               scenario=OXYScenario)

## DAQ TRANSFER TEST PDs (fall 2024)
DATASETS_DAQ_TFTEST = ["TestHLTPhysics0","TestHLTPhysics1", "TestHLTPhysics2", "TestHLTPhysics3",
            "TestHLTPhysics4", "TestHLTPhysics5", "TestHLTPhysics6","TestHLTPhysics7",
            "TestHLTPhysics8", "TestHLTPhysics9","TestHLTPhysics10","TestHLTPhysics11",
            "TestHLTPhysics12", "TestHLTPhysics13","TestHLTPhysics14","TestHLTPhysics15",
            "TestHLTPhysics16", "TestHLTPhysics17","TestHLTPhysics18","TestHLTPhysics19",
            "TestHLTPhysics20", "TestHLTPhysics21","TestHLTPhysics22","TestHLTPhysics23",
            "TestHLTPhysics24", "TestHLTPhysics25","TestHLTPhysics26","TestHLTPhysics27",
            "TestHLTPhysics28", "TestHLTPhysics29","TestHLTPhysics30","TestHLTPhysics31",
            "TestHLTPhysics32", "TestHLTPhysics33","TestHLTPhysics34","TestHLTPhysics35",
            "TestHLTPhysics36", "TestHLTPhysics37","TestHLTPhysics38","TestHLTPhysics39"]

for dataset in DATASETS_DAQ_TFTEST:
    addDataset(tier0Config, dataset,
               do_reco=False,
               raw_to_disk=False,
               dqm_sequences=["@none"],
               scenario=OXYScenario)


########################################################
### SpecialRandom PDs                                ###
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
               scenario=OXYScenario)

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
               scenario=OXYScenario)

DATASETS = ["SpecialMinimumBias0", "SpecialMinimumBias1", "SpecialMinimumBias2", "SpecialMinimumBias3"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               alca_producers=["TkAlMinBias"]
               )
               
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
	     "SpecialZeroBias17", "SpecialZeroBias18", "SpecialZeroBias19",
	     "SpecialZeroBias20", "SpecialZeroBias21", "SpecialZeroBias22",
	     "SpecialZeroBias23", "SpecialZeroBias24", "SpecialZeroBias25",
	     "SpecialZeroBias26", "SpecialZeroBias27", "SpecialZeroBias28",
	     "SpecialZeroBias29", "SpecialZeroBias30", "SpecialZeroBias31"]

DATASETS += ["PPRefZeroBiasPlusForward0", "PPRefZeroBiasPlusForward1", "PPRefZeroBiasPlusForward2",
             "PPRefZeroBiasPlusForward3", "PPRefZeroBiasPlusForward4", "PPRefZeroBiasPlusForward5", "PPRefZeroBiasPlusForward6",
             "PPRefZeroBiasPlusForward7", "PPRefZeroBiasPlusForward8", "PPRefZeroBiasPlusForward9", "PPRefZeroBiasPlusForward10",
             "PPRefZeroBiasPlusForward11", "PPRefZeroBiasPlusForward12", "PPRefZeroBiasPlusForward13", "PPRefZeroBiasPlusForward14",
             "PPRefZeroBiasPlusForward15", "PPRefZeroBiasPlusForward16", "PPRefZeroBiasPlusForward17", "PPRefZeroBiasPlusForward18",
             "PPRefZeroBiasPlusForward19", "PPRefZeroBiasPlusForward20", "PPRefZeroBiasPlusForward21", "PPRefZeroBiasPlusForward22",
             "PPRefZeroBiasPlusForward23", "PPRefZeroBiasPlusForward24"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               raw_to_disk=True,
               write_reco=False,
               write_dqm=True,
               dqm_sequences=["@commonSiStripZeroBias", "@ecal", "@hcal", "@muon", "@jetmet", "@ctpps"],
               alca_producers=["SiStripCalZeroBias", "TkAlMinBias", "SiStripCalMinBias", "LumiPixelsMinBias",
                               "HcalCalIsolatedBunchSelector"],
               physics_skims=["LogError", "LogErrorMonitor"],
               timePerEvent=3.5,
               sizePerEvent=1500,
               scenario=ppRefScenario)

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
               scenario=OXYScenario)

#################### SPECIAL RUNS ######################

########################################################
### Special Oxygen and Neon Datasets Here            ###
########################################################

DATASETS = ["IonPhysics0"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
                do_reco=True,
                write_reco=False, 
                write_aod=True, 
                write_miniaod=True, 
                write_nanoaod=True, 
                write_dqm=True,
                dqm_sequences=["@common", "@muon", "@lumi", "@L1TMuon", "@jetmet", "@egamma", "@L1TMon", "@hcal", "@ecal", "@ctpps"],
                alca_producers=["TkAlMuonIsolated", "SiPixelCalSingleMuonLoose", "SiPixelCalSingleMuonTight", "TkAlZMuMu", 
                "TkAlDiMuonAndVertex", "TkAlJetHT", "TkAlJpsiMuMu", "TkAlUpsilonMuMu", "SiStripCalZeroBias", "TkAlMinBias", "SiStripCalMinBias"],
                physics_skims=["LogError", "LogErrorMonitor", "IonHighPtMuon", "IonDimuon"],
                raw_to_disk=False,
                aod_to_disk=True,
                nano_flavours=['@PHYS', '@L1'],
                scenario=OXYScenario)

DATASETS = ["IonPhysics1", "IonPhysics2", "IonPhysics3", "IonPhysics4",
            "IonPhysics5", "IonPhysics6", "IonPhysics7", "IonPhysics8", "IonPhysics9",
            "IonPhysics10", "IonPhysics11", "IonPhysics12", "IonPhysics13", "IonPhysics14",
            "IonPhysics15", "IonPhysics16", "IonPhysics17", "IonPhysics18", "IonPhysics19",
            "IonPhysics20", "IonPhysics21", "IonPhysics22", "IonPhysics23", "IonPhysics24",
            "IonPhysics25", "IonPhysics26", "IonPhysics27", "IonPhysics28", "IonPhysics29",
            "IonPhysics30", "IonPhysics31", "IonPhysics32", "IonPhysics33", "IonPhysics34",
            "IonPhysics35", "IonPhysics36", "IonPhysics37", "IonPhysics38", "IonPhysics39",
            "IonPhysics40", "IonPhysics41", "IonPhysics42", "IonPhysics43", "IonPhysics44",
            "IonPhysics45", "IonPhysics46", "IonPhysics47", "IonPhysics48", "IonPhysics49",
            "IonPhysics50", "IonPhysics51", "IonPhysics52", "IonPhysics53", "IonPhysics54",
            "IonPhysics55", "IonPhysics56", "IonPhysics57", "IonPhysics58", "IonPhysics59"
]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
                do_reco=True,
                write_reco=False, 
                write_aod=True, 
                write_miniaod=True, 
                write_nanoaod=True, 
                write_dqm=False,
                dqm_sequences=["@none"],
                alca_producers=["TkAlMuonIsolated", "SiPixelCalSingleMuonTight", "TkAlZMuMu", 
                "TkAlDiMuonAndVertex", "TkAlJpsiMuMu", "TkAlUpsilonMuMu"],
                physics_skims=["LogError", "LogErrorMonitor", "IonHighPtMuon", "IonDimuon"],
                raw_to_disk=False,
                aod_to_disk=True,
                nano_flavours=['@PHYS', '@L1'],
                scenario=OXYScenario)



########################################################

########################################################
### Parking and Scouting PDs                         ###
########################################################

DATASETS = ["L1Scouting"]
for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False)

DATASETS = ["L1ScoutingSelection"]
for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False)

DATASETS = ["ScoutingPFRun3"] # From stream ScoutingPF --> Repacked to HLTSCOUT

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_aod=False,
               write_miniaod=False,
               scenario=hltScoutingScenario)

DATASETS = ["RPCMonitor"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               scenario=OXYScenario)

DATASETS = ["ScoutingPFMonitor"] # From Stream PhysicsScoutingPFMonitor --> repacked to RAW

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               dqm_sequences=["@common", "@hltScouting"],
               nano_flavours=['@PHYS', '@L1', '@ScoutMonitor'],
               write_reco=False, write_aod=False, write_miniaod=True, write_dqm=True,
               scenario=OXYScenario)

DATASETS = ["ScoutingCaloCommissioning", "ScoutingCaloHT", "ScoutingCaloMuon",
            "ScoutingPFCommissioning", "ScoutingPFHT", "ScoutingPFMuon"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               scenario=OXYScenario)

DATASETS = ["AlCaElectron", "VRRandom", "VRRandom0", "VRRandom1", "VRRandom2", "VRRandom3",
             "VRRandom4", "VRRandom5", "VRRandom6", "VRRandom7", "VRRandom8", "VRRandom9",
             "VRRandom10", "VRRandom11", "VRRandom12", "VRRandom13", "VRRandom14", "VRRandom15",
             "VRZeroBias", "VirginRaw"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               scenario=OXYScenario)

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

#####################################
### RAW Skim / Secondary Datasets ###
#####################################

RAWSKIM_DATASETS = ["ParkingDoubleMuonLowMass0-ReserveDMu", "ParkingDoubleMuonLowMass1-ReserveDMu",
                    "ParkingDoubleMuonLowMass2-ReserveDMu", "ParkingDoubleMuonLowMass3-ReserveDMu",
                    "ParkingDoubleMuonLowMass4-ReserveDMu", "ParkingDoubleMuonLowMass5-ReserveDMu",
                    "ParkingDoubleMuonLowMass6-ReserveDMu", "ParkingDoubleMuonLowMass7-ReserveDMu"]
for rawSkimDataset in RAWSKIM_DATASETS:
    addDataset(tier0Config, rawSkimDataset,
               do_reco=False,
               write_dqm=True,
               archival_node=None,
               tape_node=None,
               scenario=OXYScenario)

#######################
### ignored streams ###
#######################

# Define streams to be ignored by MainAgent and processed by a HelperAgent if any.
setHelperAgentStreams(tier0Config, {'SecondAgent': [],
                                    'ThirdAgent' : []
                                   })

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
ignoreStream(tier0Config, "DQMPPSRandom")
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
