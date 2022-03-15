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
from T0.RunConfig.Tier0Config import addRepackConfig
from T0.RunConfig.Tier0Config import addExpressConfig
from T0.RunConfig.Tier0Config import setInjectRuns
from T0.RunConfig.Tier0Config import setStreamerPNN
from T0.RunConfig.Tier0Config import setEnableUniqueWorkflowName
from T0.RunConfig.Tier0Config import addSiteConfig
from T0.RunConfig.Tier0Config import setStorageSite
from T0.RunConfig.Tier0Config import setScramArch

# Create the Tier0 configuration object
tier0Config = createTier0Config()

# Set the verstion configuration (not used at the moment)
setConfigVersion(tier0Config, "replace with real version")

# Set run number to replay
setInjectRuns(tier0Config, [324841])

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
setAcquisitionEra(tier0Config, "Tier0_REPLAY_2022")
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
    'default': "CMSSW_12_2_1_patch2"
}

# Configure ScramArch
setDefaultScramArch(tier0Config, "slc7_amd64_gcc630")
setScramArch(tier0Config, defaultCMSSWVersion['default'], "slc7_amd64_gcc900")

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
dt = 213
defaultProcVersion = dt
expressProcVersion = dt
alcarawProcVersion = dt

# Defaults for GlobalTag
expressGlobalTag = "122X_dataRun3_Express_TIER0_REPLAY_Run2_v1"
promptrecoGlobalTag = "122X_dataRun3_Prompt_TIER0_REPLAY_Run2_v1"
alcap0GlobalTag = "122X_dataRun3_Prompt_TIER0_REPLAY_Run2_v1"

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
    "CMSSW_11_3_4" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_0" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_1" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_2" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_2_patch1" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_2_patch2" : defaultCMSSWVersion['default']
    }

expressVersionOverride = {
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
    "CMSSW_11_3_4" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_0" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_1" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_2" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_2" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_2_patch1" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_2_patch2" : defaultCMSSWVersion['default']
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
           disk_node="T0_CH_CERN_Disk",
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
                 diskNode="T2_CH_CERN",
                 data_tiers=["FEVT"],
                 write_dqm=True,
                 alca_producers=["SiStripPCLHistos", "SiStripCalZeroBias", "SiStripCalMinBias", "SiStripCalMinBiasAAG",
                                 "TkAlMinBias", "LumiPixelsMinBias", "SiPixelCalZeroBias","SiPixelCalSingleMuon",
                                 "PromptCalibProd", "PromptCalibProdSiStrip", "PromptCalibProdSiPixelAli",
                                 "PromptCalibProdSiStripGains", "PromptCalibProdSiStripGainsAAG",
                                 "PromptCalibProdSiPixel", "PromptCalibProdSiPixelLorentzAngle"
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
ignoreStream(tier0Config, "HIExpress")
ignoreStream(tier0Config, "HIExpressAlignment")
ignoreStream(tier0Config, "BTagCSV")
ignoreStream(tier0Config,"ALCALumiPixelsCountsExpress1")
ignoreStream(tier0Config,"ALCALumiPixelsCountsExpress10")
ignoreStream(tier0Config,"ALCALumiPixelsCountsExpress11")
ignoreStream(tier0Config,"ALCALumiPixelsCountsExpress12")
ignoreStream(tier0Config,"ALCALumiPixelsCountsExpress2")
ignoreStream(tier0Config,"ALCALumiPixelsCountsExpress3")
ignoreStream(tier0Config,"ALCALumiPixelsCountsExpress4")
ignoreStream(tier0Config,"ALCALumiPixelsCountsExpress5")
ignoreStream(tier0Config,"ALCALumiPixelsCountsExpress6")
ignoreStream(tier0Config,"ALCALumiPixelsCountsExpress7")
ignoreStream(tier0Config,"ALCALumiPixelsCountsExpress8")
ignoreStream(tier0Config,"ALCALumiPixelsCountsExpress9")
ignoreStream(tier0Config,"ALCALumiPixelsCountsPrompt")
ignoreStream(tier0Config,"ALCALumiPixelsCountsPrompt1")
ignoreStream(tier0Config,"ALCALumiPixelsCountsPrompt10")
ignoreStream(tier0Config,"ALCALumiPixelsCountsPrompt11")
ignoreStream(tier0Config,"ALCALumiPixelsCountsPrompt12")
ignoreStream(tier0Config,"ALCALumiPixelsCountsPrompt2")
ignoreStream(tier0Config,"ALCALumiPixelsCountsPrompt3")
ignoreStream(tier0Config,"ALCALumiPixelsCountsPrompt4")
ignoreStream(tier0Config,"ALCALumiPixelsCountsPrompt5")
ignoreStream(tier0Config,"ALCALumiPixelsCountsPrompt6")
ignoreStream(tier0Config,"ALCALumiPixelsCountsPrompt7")
ignoreStream(tier0Config,"ALCALumiPixelsCountsPrompt8")
ignoreStream(tier0Config,"ALCALumiPixelsCountsPrompt9")
ignoreStream(tier0Config,"AlCaLumiPixels0")
ignoreStream(tier0Config,"AlCaLumiPixels1")
ignoreStream(tier0Config,"AlCaLumiPixels10")
ignoreStream(tier0Config,"AlCaLumiPixels11")
ignoreStream(tier0Config,"AlCaLumiPixels12")
ignoreStream(tier0Config,"AlCaLumiPixels2")
ignoreStream(tier0Config,"AlCaLumiPixels3")
ignoreStream(tier0Config,"AlCaLumiPixels4")
ignoreStream(tier0Config,"AlCaLumiPixels5")
ignoreStream(tier0Config,"AlCaLumiPixels6")
ignoreStream(tier0Config,"AlCaLumiPixels7")
ignoreStream(tier0Config,"AlCaLumiPixels8")
ignoreStream(tier0Config,"AlCaLumiPixels9")
ignoreStream(tier0Config,"AlCaPCCZeroBiasFromRECO")
ignoreStream(tier0Config,"AlCaPCCZeroBiasFromRECO")
ignoreStream(tier0Config,"BPHSkim")
ignoreStream(tier0Config,"Commissioning2")
ignoreStream(tier0Config,"Commissioning3")
ignoreStream(tier0Config,"Commissioning4")
ignoreStream(tier0Config,"CommissioningDoubleJet")
ignoreStream(tier0Config,"CommissioningEGamma")
ignoreStream(tier0Config,"CommissioningMuons")
ignoreStream(tier0Config,"CommissioningSingleJet")
ignoreStream(tier0Config,"CommissioningTaus")
ignoreStream(tier0Config,"CosmicTP")
ignoreStream(tier0Config,"EGMLowPU")
ignoreStream(tier0Config,"EcalCalEtaCalib")
ignoreStream(tier0Config,"EcalESAlign")
ignoreStream(tier0Config,"EcalESAlign")
ignoreStream(tier0Config,"EcalLaser")
ignoreStream(tier0Config,"EcalUncalWElectron")
ignoreStream(tier0Config,"EcalUncalWElectron")
ignoreStream(tier0Config,"EcalUncalZElectron")
ignoreStream(tier0Config,"EphemeralHLTPhysics2")
ignoreStream(tier0Config,"EphemeralHLTPhysics3")
ignoreStream(tier0Config,"EphemeralHLTPhysics4")
ignoreStream(tier0Config,"EphemeralHLTPhysics5")
ignoreStream(tier0Config,"EphemeralHLTPhysics6")
ignoreStream(tier0Config,"EphemeralHLTPhysics7")
ignoreStream(tier0Config,"EphemeralHLTPhysics8")
ignoreStream(tier0Config,"EphemeralZeroBias2")
ignoreStream(tier0Config,"EphemeralZeroBias3")
ignoreStream(tier0Config,"EphemeralZeroBias4")
ignoreStream(tier0Config,"EphemeralZeroBias5")
ignoreStream(tier0Config,"EphemeralZeroBias6")
ignoreStream(tier0Config,"EphemeralZeroBias7")
ignoreStream(tier0Config,"EphemeralZeroBias8")
ignoreStream(tier0Config,"ExpressPA")
ignoreStream(tier0Config,"FSQJet2")
ignoreStream(tier0Config,"FullTrack")
ignoreStream(tier0Config,"HIExpressAlignment")
ignoreStream(tier0Config,"HINCaloJet100")
ignoreStream(tier0Config,"HINCaloJetsOther")
ignoreStream(tier0Config,"HINPFJet100")
ignoreStream(tier0Config,"HINPFJets")
ignoreStream(tier0Config,"HITestReduced")
ignoreStream(tier0Config,"HIZeroBias10")
ignoreStream(tier0Config,"HIZeroBias11")
ignoreStream(tier0Config,"HIZeroBias12")
ignoreStream(tier0Config,"HIZeroBias2")
ignoreStream(tier0Config,"HIZeroBias3")
ignoreStream(tier0Config,"HIZeroBias4")
ignoreStream(tier0Config,"HIZeroBias5")
ignoreStream(tier0Config,"HIZeroBias6")
ignoreStream(tier0Config,"HIZeroBias7")
ignoreStream(tier0Config,"HIZeroBias8")
ignoreStream(tier0Config,"HIZeroBias9")
ignoreStream(tier0Config,"HLTMonitorPA")
ignoreStream(tier0Config,"HLTPhysics0")
ignoreStream(tier0Config,"HLTPhysics1")
ignoreStream(tier0Config,"HLTPhysics10")
ignoreStream(tier0Config,"HLTPhysics2")
ignoreStream(tier0Config,"HLTPhysics3")
ignoreStream(tier0Config,"HLTPhysics4")
ignoreStream(tier0Config,"HLTPhysics5")
ignoreStream(tier0Config,"HLTPhysics6")
ignoreStream(tier0Config,"HLTPhysics7")
ignoreStream(tier0Config,"HLTPhysics8")
ignoreStream(tier0Config,"HLTPhysics9")
ignoreStream(tier0Config,"HLTPhysicsCosmics1")
ignoreStream(tier0Config,"HLTPhysicsCosmics2")
ignoreStream(tier0Config,"HLTPhysicsCosmics3")
ignoreStream(tier0Config,"HLTPhysicsCosmics4")
ignoreStream(tier0Config,"HLTPhysicsCosmics5")
ignoreStream(tier0Config,"HLTPhysicsCosmics6")
ignoreStream(tier0Config,"HLTPhysicsCosmics7")
ignoreStream(tier0Config,"HLTPhysicsCosmics8")
ignoreStream(tier0Config,"HLTPhysicsIsolatedBunch")
ignoreStream(tier0Config,"HLTPhysicspart1")
ignoreStream(tier0Config,"HLTPhysicspart2")
ignoreStream(tier0Config,"HLTPhysicspart3")
ignoreStream(tier0Config,"HLTPhysicspart4")
ignoreStream(tier0Config,"HLTPhysicspart5")
ignoreStream(tier0Config,"HLTPhysicspart6")
ignoreStream(tier0Config,"HLTPhysicspart7")
ignoreStream(tier0Config,"HcalCalHBHEMuonFilter")
ignoreStream(tier0Config,"HcalCalHBHEMuonFilter")
ignoreStream(tier0Config,"HcalCalHO")
ignoreStream(tier0Config,"HcalCalHO")
ignoreStream(tier0Config,"HcalCalIsoTrk")
ignoreStream(tier0Config,"HcalCalIsoTrkFilter")
ignoreStream(tier0Config,"HcalCalIsoTrkFilter")
ignoreStream(tier0Config,"HcalCalIsoTrkFilter")
ignoreStream(tier0Config,"HcalCalIsoTrkFilter")
ignoreStream(tier0Config,"HcalCalIsoTrkFilter")
ignoreStream(tier0Config,"HcalCalIsolatedBunchFilter")
ignoreStream(tier0Config,"HcalCalIsolatedBunchSelector")
ignoreStream(tier0Config,"HcalCalIterativePhiSym")
ignoreStream(tier0Config,"HcalCalIterativePhiSym")
ignoreStream(tier0Config,"HcalCalIterativePhiSym")
ignoreStream(tier0Config,"HcalCalIterativePhiSym")
ignoreStream(tier0Config,"HcalCalIterativePhiSym")
ignoreStream(tier0Config,"HcalCalIterativePhiSym")
ignoreStream(tier0Config,"HcalCalIterativePhiSym")
ignoreStream(tier0Config,"HcalCalPedestal")
ignoreStream(tier0Config,"HeavyFlavor")
ignoreStream(tier0Config,"HighMET")
ignoreStream(tier0Config,"HighMultiplicity85EOF")
ignoreStream(tier0Config,"HighMultiplicityEOF1")
ignoreStream(tier0Config,"HighMultiplicityEOF2")
ignoreStream(tier0Config,"HighMultiplicityEOF3")
ignoreStream(tier0Config,"HighMultiplicityEOF4")
ignoreStream(tier0Config,"HighMultiplicityEOF5")
ignoreStream(tier0Config,"L1MinimumBias1")
ignoreStream(tier0Config,"L1MinimumBias10")
ignoreStream(tier0Config,"L1MinimumBias2")
ignoreStream(tier0Config,"L1MinimumBias3")
ignoreStream(tier0Config,"L1MinimumBias4")
ignoreStream(tier0Config,"L1MinimumBias5")
ignoreStream(tier0Config,"L1MinimumBias6")
ignoreStream(tier0Config,"L1MinimumBias7")
ignoreStream(tier0Config,"L1MinimumBias8")
ignoreStream(tier0Config,"L1MinimumBias9")
ignoreStream(tier0Config,"L1MinimumBiasHF2")
ignoreStream(tier0Config,"L1MinimumBiasHF3")
ignoreStream(tier0Config,"L1MinimumBiasHF4")
ignoreStream(tier0Config,"L1MinimumBiasHF5")
ignoreStream(tier0Config,"L1MinimumBiasHF6")
ignoreStream(tier0Config,"L1MinimumBiasHF7")
ignoreStream(tier0Config,"L1MinimumBiasHF8")
ignoreStream(tier0Config,"LogError")
ignoreStream(tier0Config,"LogError")
ignoreStream(tier0Config,"LogError")
ignoreStream(tier0Config,"LogError")
ignoreStream(tier0Config,"LogError")
ignoreStream(tier0Config,"LogError")
ignoreStream(tier0Config,"LogError")
ignoreStream(tier0Config,"LogError")
ignoreStream(tier0Config,"LogError")
ignoreStream(tier0Config,"LogError")
ignoreStream(tier0Config,"LogError")
ignoreStream(tier0Config,"LogError")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LogErrorMonitor")
ignoreStream(tier0Config,"LowEGJet")
ignoreStream(tier0Config,"LumiPixelsMinBias")
ignoreStream(tier0Config,"LumiPixelsMinBias")
ignoreStream(tier0Config,"LumiPixelsMinBias")
ignoreStream(tier0Config,"MinimumBias0")
ignoreStream(tier0Config,"MinimumBias1")
ignoreStream(tier0Config,"MinimumBias10")
ignoreStream(tier0Config,"MinimumBias11")
ignoreStream(tier0Config,"MinimumBias12")
ignoreStream(tier0Config,"MinimumBias13")
ignoreStream(tier0Config,"MinimumBias14")
ignoreStream(tier0Config,"MinimumBias15")
ignoreStream(tier0Config,"MinimumBias16")
ignoreStream(tier0Config,"MinimumBias17")
ignoreStream(tier0Config,"MinimumBias18")
ignoreStream(tier0Config,"MinimumBias19")
ignoreStream(tier0Config,"MinimumBias2")
ignoreStream(tier0Config,"MinimumBias20")
ignoreStream(tier0Config,"MinimumBias3")
ignoreStream(tier0Config,"MinimumBias4")
ignoreStream(tier0Config,"MinimumBias5")
ignoreStream(tier0Config,"MinimumBias6")
ignoreStream(tier0Config,"MinimumBias7")
ignoreStream(tier0Config,"MinimumBias8")
ignoreStream(tier0Config,"MinimumBias9")
ignoreStream(tier0Config,"MinimumBiasTotem")
ignoreStream(tier0Config,"MuAlCalIsolatedMu")
ignoreStream(tier0Config,"MuAlCalIsolatedMu")
ignoreStream(tier0Config,"MuAlCalIsolatedMu")
ignoreStream(tier0Config,"MuAlCalIsolatedMu")
ignoreStream(tier0Config,"MuAlCalIsolatedMu")
ignoreStream(tier0Config,"MuAlCalIsolatedMu")
ignoreStream(tier0Config,"MuAlGlobalCosmics")
ignoreStream(tier0Config,"MuAlOverlaps")
ignoreStream(tier0Config,"MuAlOverlaps")
ignoreStream(tier0Config,"MuAlOverlaps")
ignoreStream(tier0Config,"MuAlOverlaps")
ignoreStream(tier0Config,"MuAlOverlaps")
ignoreStream(tier0Config,"MuAlOverlaps")
ignoreStream(tier0Config,"MuAlZMuMu")
ignoreStream(tier0Config,"MuAlZMuMu")
ignoreStream(tier0Config,"MuAlZMuMu")
ignoreStream(tier0Config,"MuAlZMuMu")
ignoreStream(tier0Config,"MuAlZMuMu")
ignoreStream(tier0Config,"MuAlZMuMu")
ignoreStream(tier0Config,"MuPlusX")
ignoreStream(tier0Config,"MuTau")
ignoreStream(tier0Config,"MuonPOGJPsiSkim")
ignoreStream(tier0Config,"PACastor")
ignoreStream(tier0Config,"PADTrack2")
ignoreStream(tier0Config,"PADoubleMuOpen")
ignoreStream(tier0Config,"PADoubleMuon")
ignoreStream(tier0Config,"PAEGJet1")
ignoreStream(tier0Config,"PAEmptyBX")
ignoreStream(tier0Config,"PAForward")
ignoreStream(tier0Config,"PAHighMultiplicity1")
ignoreStream(tier0Config,"PAHighMultiplicity2")
ignoreStream(tier0Config,"PAHighMultiplicity3")
ignoreStream(tier0Config,"PAHighMultiplicity4")
ignoreStream(tier0Config,"PAHighMultiplicity5")
ignoreStream(tier0Config,"PAHighMultiplicity6")
ignoreStream(tier0Config,"PAHighMultiplicity7")
ignoreStream(tier0Config,"PAL1AlwaysTrue1")
ignoreStream(tier0Config,"PAL1AlwaysTrue2")
ignoreStream(tier0Config,"PAL1AlwaysTrue3")
ignoreStream(tier0Config,"PAL1AlwaysTrue4")
ignoreStream(tier0Config,"PAL1AlwaysTrue5")
ignoreStream(tier0Config,"PAL1AlwaysTrue6")
ignoreStream(tier0Config,"PAL1AlwaysTrue7")
ignoreStream(tier0Config,"PAL1AlwaysTrue8")
ignoreStream(tier0Config,"PAL1AlwaysTrue9")
ignoreStream(tier0Config,"PAMinimumBias10")
ignoreStream(tier0Config,"PAMinimumBias11")
ignoreStream(tier0Config,"PAMinimumBias12")
ignoreStream(tier0Config,"PAMinimumBias13")
ignoreStream(tier0Config,"PAMinimumBias14")
ignoreStream(tier0Config,"PAMinimumBias15")
ignoreStream(tier0Config,"PAMinimumBias16")
ignoreStream(tier0Config,"PAMinimumBias17")
ignoreStream(tier0Config,"PAMinimumBias18")
ignoreStream(tier0Config,"PAMinimumBias19")
ignoreStream(tier0Config,"PAMinimumBias2")
ignoreStream(tier0Config,"PAMinimumBias20")
ignoreStream(tier0Config,"PAMinimumBias3")
ignoreStream(tier0Config,"PAMinimumBias4")
ignoreStream(tier0Config,"PAMinimumBias5")
ignoreStream(tier0Config,"PAMinimumBias6")
ignoreStream(tier0Config,"PAMinimumBias7")
ignoreStream(tier0Config,"PAMinimumBias8")
ignoreStream(tier0Config,"PAMinimumBias9")
ignoreStream(tier0Config,"PAMinimumBiasBkg")
ignoreStream(tier0Config,"PAMinimumBiasHFOR1")
ignoreStream(tier0Config,"PAMinimumBiasHFOR2")
ignoreStream(tier0Config,"PASingleMuon")
ignoreStream(tier0Config,"PAZeroBias1")
ignoreStream(tier0Config,"PAZeroBias2")
ignoreStream(tier0Config,"PAZeroBias3")
ignoreStream(tier0Config,"PAZeroBias4")
ignoreStream(tier0Config,"PAZeroBias5")
ignoreStream(tier0Config,"PAZeroBias6")
ignoreStream(tier0Config,"PAZeroBias7")
ignoreStream(tier0Config,"PAZeroBias8")
ignoreStream(tier0Config,"PAZeroBias9")
ignoreStream(tier0Config,"ParkingBPH2")
ignoreStream(tier0Config,"ParkingBPH3")
ignoreStream(tier0Config,"ParkingBPH4")
ignoreStream(tier0Config,"ParkingBPH5")
ignoreStream(tier0Config,"ParkingBPH6")
ignoreStream(tier0Config,"ParkingHLTPhysics0")
ignoreStream(tier0Config,"ParkingHLTPhysics1")
ignoreStream(tier0Config,"ParkingHLTPhysics10")
ignoreStream(tier0Config,"ParkingHLTPhysics11")
ignoreStream(tier0Config,"ParkingHLTPhysics12")
ignoreStream(tier0Config,"ParkingHLTPhysics13")
ignoreStream(tier0Config,"ParkingHLTPhysics14")
ignoreStream(tier0Config,"ParkingHLTPhysics15")
ignoreStream(tier0Config,"ParkingHLTPhysics16")
ignoreStream(tier0Config,"ParkingHLTPhysics17")
ignoreStream(tier0Config,"ParkingHLTPhysics18")
ignoreStream(tier0Config,"ParkingHLTPhysics19")
ignoreStream(tier0Config,"ParkingHLTPhysics2")
ignoreStream(tier0Config,"ParkingHLTPhysics20")
ignoreStream(tier0Config,"ParkingHT430to450")
ignoreStream(tier0Config,"ParkingHT450to470")
ignoreStream(tier0Config,"ParkingHT470to500")
ignoreStream(tier0Config,"ParkingHT500to550")
ignoreStream(tier0Config,"ParkingHT650")
ignoreStream(tier0Config,"ParkingZeroBias0")
ignoreStream(tier0Config,"ParkingZeroBias1")
ignoreStream(tier0Config,"ParkingZeroBias10")
ignoreStream(tier0Config,"ParkingZeroBias11")
ignoreStream(tier0Config,"ParkingZeroBias12")
ignoreStream(tier0Config,"ParkingZeroBias13")
ignoreStream(tier0Config,"ParkingZeroBias14")
ignoreStream(tier0Config,"ParkingZeroBias15")
ignoreStream(tier0Config,"ParkingZeroBias16")
ignoreStream(tier0Config,"ParkingZeroBias17")
ignoreStream(tier0Config,"ParkingZeroBias18")
ignoreStream(tier0Config,"ParkingZeroBias19")
ignoreStream(tier0Config,"ParkingZeroBias2")
ignoreStream(tier0Config,"ParkingZeroBias20")
ignoreStream(tier0Config,"SiPixelCalCosmics")
ignoreStream(tier0Config,"SiStripCalMinBias")
ignoreStream(tier0Config,"SiStripCalMinBias")
ignoreStream(tier0Config,"SiStripCalMinBias")
ignoreStream(tier0Config,"SiStripCalMinBias")
ignoreStream(tier0Config,"SiStripCalMinBias")
ignoreStream(tier0Config,"SiStripCalMinBiasAfterAbortGap")
ignoreStream(tier0Config,"SiStripPCLHistos")
ignoreStream(tier0Config,"SingleMuHighPt")
ignoreStream(tier0Config,"SingleMuLowPt")
ignoreStream(tier0Config,"SingleMuonTnP")
ignoreStream(tier0Config,"SingleTrack")
ignoreStream(tier0Config,"TOTEM11")
ignoreStream(tier0Config,"TOTEM12")
ignoreStream(tier0Config,"TOTEM13")
ignoreStream(tier0Config,"TOTEM20")
ignoreStream(tier0Config,"TOTEM21")
ignoreStream(tier0Config,"TOTEM22")
ignoreStream(tier0Config,"TOTEM23")
ignoreStream(tier0Config,"TOTEM3")
ignoreStream(tier0Config,"TOTEM40")
ignoreStream(tier0Config,"TOTEM41")
ignoreStream(tier0Config,"TOTEM42")
ignoreStream(tier0Config,"TOTEM43")
ignoreStream(tier0Config,"TkAlCosmics0T")
ignoreStream(tier0Config,"TkAlJpsiMuMu")
ignoreStream(tier0Config,"TkAlMinBias")
ignoreStream(tier0Config,"TkAlMinBias")
ignoreStream(tier0Config,"TkAlMinBias")
ignoreStream(tier0Config,"TkAlMinBias")
ignoreStream(tier0Config,"TkAlMinBias")
ignoreStream(tier0Config,"TkAlMinBias")
ignoreStream(tier0Config,"TkAlUpsilonMuMu")
ignoreStream(tier0Config,"TkAlUpsilonMuMuPA")
ignoreStream(tier0Config,"TkAlZMuMuPA")
ignoreStream(tier0Config,"ToTOTEM")
ignoreStream(tier0Config,"ToTOTEM_DoubleJet32_0")
ignoreStream(tier0Config,"ToTOTEM_DoubleJet32_1")
ignoreStream(tier0Config,"ToTOTEM_DoubleJet32_2")
ignoreStream(tier0Config,"ToTOTEM_DoubleJet32_3")
ignoreStream(tier0Config,"Totem2")
ignoreStream(tier0Config,"Totem3")
ignoreStream(tier0Config,"Totem34")
ignoreStream(tier0Config,"Totem4")
ignoreStream(tier0Config,"ZElectron")
ignoreStream(tier0Config,"ZMu")
ignoreStream(tier0Config,"ZeroBias1")
ignoreStream(tier0Config,"ZeroBias10")
ignoreStream(tier0Config,"ZeroBias11")
ignoreStream(tier0Config,"ZeroBias12")
ignoreStream(tier0Config,"ZeroBias13")
ignoreStream(tier0Config,"ZeroBias14")
ignoreStream(tier0Config,"ZeroBias15")
ignoreStream(tier0Config,"ZeroBias16")
ignoreStream(tier0Config,"ZeroBias17")
ignoreStream(tier0Config,"ZeroBias18")
ignoreStream(tier0Config,"ZeroBias19")
ignoreStream(tier0Config,"ZeroBias2")
ignoreStream(tier0Config,"ZeroBias20")
ignoreStream(tier0Config,"ZeroBiasPixelHVScan1")
ignoreStream(tier0Config,"ZeroBiasPixelHVScan2")
ignoreStream(tier0Config,"ZeroBiasPixelHVScan3")
ignoreStream(tier0Config,"ZeroBiasPixelHVScan4")
ignoreStream(tier0Config,"ZeroBiasPixelHVScan5")
ignoreStream(tier0Config,"ZeroBiasPixelHVScan6")
ignoreStream(tier0Config,"ZeroBiasPixelHVScan7")
ignoreStream(tier0Config,"ZeroBiasTotem")


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
