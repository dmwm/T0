"""
_OfflineConfiguration_
Processing configuration for the Tier0 - Replay version
"""
from __future__ import print_function

import datetime
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
from T0.RunConfig.Tier0Config import addSiteConfig
from T0.RunConfig.Tier0Config import setInjectRuns
from T0.RunConfig.Tier0Config import setStreamerPNN
from T0.RunConfig.Tier0Config import setStorageSite
from T0.RunConfig.Tier0Config import setEnableUniqueWorkflowName

# Create the Tier0 configuration object
tier0Config = createTier0Config()

# Set the verstion configuration (not used at the moment)
setConfigVersion(tier0Config, "replace with real version")

# Set run number to replay
setInjectRuns(tier0Config, [ 317696 ])

# Settings up sites
processingSite = "T2_CH_CERN"
storageSite = "T0_CH_CERN_Disk"
streamerPNN = "T0_CH_CERN_Disk"

addSiteConfig(tier0Config, "T0_CH_CERN_Disk",
                siteLocalConfig="/cvmfs/cms.cern.ch/SITECONF/T0_CH_CERN/JobConfig/site-local-config.xml",
                overrideCatalog="trivialcatalog_file:/cvmfs/cms.cern.ch/SITECONF/T0_CH_CERN/PhEDEx/storage.xml?protocol=eos"
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
setAcquisitionEra(tier0Config, "Tier0_REPLAY_2021")
setBaseRequestPriority(tier0Config, 251000)
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
setDQMUploadUrl(tier0Config, "https://cmsweb.cern.ch/dqm/dev;https://cmsweb-testbed.cern.ch/dqm/offline-test")

# PCL parameters
setPromptCalibrationConfig(tier0Config,
                           alcaHarvestTimeout=12*3600,
                           alcaHarvestCondLFNBase="/store/unmerged/tier0_harvest",
                           alcaHarvestLumiURL="root://eoscms.cern.ch//eos/cms/store/unmerged/tier0_harvest",
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
    'default': "CMSSW_12_0_2"
}

# Configure ScramArch
from T0.RunConfig.Tier0Config import setScramArch

setDefaultScramArch(tier0Config, "slc7_amd64_gcc630")
setScramArch(tier0Config, "CMSSW_12_0_2", "slc7_amd64_gcc900")

# Configure scenarios
ppScenario = "ppEra_Run2_2018"
ppScenarioB0T = "ppEra_Run2_2018"
cosmicsScenario = "cosmicsEra_Run2_2018"
hcalnzsScenario = "hcalnzsEra_Run2_2018"
hiScenario = "ppEra_Run2_2018"
alcaTrackingOnlyScenario = "trackingOnlyEra_Run2_2018"
alcaTestEnableScenario = "AlCaTestEnable"
alcaLumiPixelsScenario = "AlCaLumiPixels"
hiTestppScenario = "ppEra_Run2_2018"

# Procesing version number replays
dt = int(datetime.datetime.now().strftime("%y%m%d%H%M"))
defaultProcVersion = dt
expressProcVersion = dt
alcarawProcVersion = dt

# Defaults for GlobalTag
expressGlobalTag = "120X_dataRun3_Express_Candidate_2021_09_30_18_36_13"
promptrecoGlobalTag = "120X_dataRun3_Prompt_Candidate_2021_10_01_08_44_53"
alcap0GlobalTag = "120X_dataRun3_Prompt_Candidate_2021_10_01_08_44_53"

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
    "CMSSW_10_1_10" : "CMSSW_11_1_0_pre8",
    "CMSSW_10_2_5" : defaultCMSSWVersion['default'],
    "CMSSW_11_0_1" : defaultCMSSWVersion['default'],
    "CMSSW_11_0_2" : defaultCMSSWVersion['default'],
    "CMSSW_11_1_3" : defaultCMSSWVersion['default'],
    "CMSSW_11_1_4" : defaultCMSSWVersion['default'],
    "CMSSW_11_1_5" : defaultCMSSWVersion['default'],
    "CMSSW_11_2_1" : defaultCMSSWVersion['default'],
    "CMSSW_11_2_2" : defaultCMSSWVersion['default'],
    "CMSSW_11_2_3" : defaultCMSSWVersion['default'],
    "CMSSW_11_2_4" : defaultCMSSWVersion['default'],
    "CMSSW_11_3_1" : defaultCMSSWVersion['default'],
    "CMSSW_11_3_2" : defaultCMSSWVersion['default'],
    "CMSSW_11_3_3" : defaultCMSSWVersion['default'],
    "CMSSW_11_3_4" : defaultCMSSWVersion['default']
    }

expressVersionOverride = {
    "CMSSW_10_1_10" : "CMSSW_11_1_0_pre8",
    "CMSSW_10_2_5" : defaultCMSSWVersion['default'],
    "CMSSW_11_0_1" : defaultCMSSWVersion['default'],
    "CMSSW_11_0_2" : defaultCMSSWVersion['default'],
    "CMSSW_11_1_3" : defaultCMSSWVersion['default'],
    "CMSSW_11_1_4" : defaultCMSSWVersion['default'],
    "CMSSW_11_1_5" : defaultCMSSWVersion['default'],
    "CMSSW_11_2_1" : defaultCMSSWVersion['default'],
    "CMSSW_11_2_2" : defaultCMSSWVersion['default'],
    "CMSSW_11_2_3" : defaultCMSSWVersion['default'],
    "CMSSW_11_2_4" : defaultCMSSWVersion['default'],
    "CMSSW_11_3_1" : defaultCMSSWVersion['default'],
    "CMSSW_11_3_2" : defaultCMSSWVersion['default'],
    "CMSSW_11_3_3" : defaultCMSSWVersion['default'],
    "CMSSW_11_3_4" : defaultCMSSWVersion['default']
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
                maxLatency=24 * 3600,
                blockCloseDelay=1200,
                maxMemory=2000,
                versionOverride=repackVersionOverride)

addDataset(tier0Config, "Default",
           do_reco=False,
           write_reco=False, write_aod=True, write_miniaod=True, write_dqm=False,
           reco_delay=defaultRecoTimeout,
           reco_delay_offset=defaultRecoLockTimeout,
           reco_split=defaultRecoSplitting,
           proc_version=defaultProcVersion,
           cmssw_version=defaultCMSSWVersion,
           multicore=numberOfCores,
           global_tag=promptrecoGlobalTag,
           global_tag_connect=globalTagConnect,
           #archival_node="T0_CH_CERN_MSS",
           #tape_node="T1_US_FNAL_MSS",
           #raw_to_disk=False,
           blockCloseDelay=1200,
           timePerEvent=5,
           sizePerEvent=1500,
           scenario=ppScenario)

#############################
### Express configuration ###
#############################

addExpressConfig(tier0Config, "Express",
                 scenario=ppScenario,
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
                 versionOverride=expressVersionOverride)

addExpressConfig(tier0Config, "ExpressPhysics",
                 scenario=ppScenario,
                 data_tiers=["FEVT"],
                 write_dqm=True,
                 alca_producers=["SiStripPCLHistos", "SiStripCalZeroBias", "SiStripCalMinBias", "SiStripCalMinBiasAAG",
                                 "TkAlMinBias", "DtCalib", "LumiPixelsMinBias", "SiPixelCalZeroBias", "PPSCalTrackBasedSel",
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
                 versionOverride=expressVersionOverride)

addExpressConfig(tier0Config, "ExpressCosmics",
                 scenario=cosmicsScenario,
                 data_tiers=["FEVT"],
                 write_dqm=True,
                 alca_producers=["SiStripPCLHistos", "SiStripCalZeroBias", "TkAlCosmics0T",
                                 "SiPixelCalZeroBias",
                                 "PromptCalibProdSiStrip", "PromptCalibProdSiPixel", "SiStripCalCosmics"
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
                 versionOverride=expressVersionOverride)

addExpressConfig(tier0Config, "HLTMonitor",
                 scenario=ppScenario,
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
                 dataType="data")

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
                 versionOverride=expressVersionOverride)

addExpressConfig(tier0Config, "ALCALUMIPIXELSEXPRESS",
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
                 versionOverride=expressVersionOverride)

#####################
### HI Tests 2018 ###
#####################

addExpressConfig(tier0Config, "HIExpress",
                 scenario=hiTestppScenario,
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
                 versionOverride=expressVersionOverride)

###################################
### Standard Physics PDs (2017) ###
###################################

DATASETS = ["DoubleMuon"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_reco=True,
               write_dqm=True,
               alca_producers=["TkAlZMuMu", "TkAlDiMuonAndVertex"],
               dqm_sequences=["@common", "@muon", "@lumi", "@L1TMuon"],
               physics_skims=["LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["SingleMuon"] # SingleMuonTnP only for 2017 ppRef run

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               write_dqm=True,
               alca_producers=["SiPixelCalSingleMuon", "SiPixelCalSingleMuonLoose", "SiPixelCalSingleMuonTight"],
               dqm_sequences=["@common", "@muon", "@lumi", "@L1TMuon"],
               physics_skims=["MuonPOGSkim", "MuTau", "ZMu", "LogError", "LogErrorMonitor"],
               scenario=ppScenario)

DATASETS = ["TestEnablesEcalHcal"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=True,
               alca_producers=["EcalTestPulsesRaw", "PromptCalibProdEcalPedestals"],
               dqm_sequences=["@common"],
               scenario=alcaTestEnableScenario)



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
