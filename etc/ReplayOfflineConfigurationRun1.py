"""
_OfflineConfiguration_

Processing configuration for the Tier0 - Replay version - Run1 Scale Tests
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
from T0.RunConfig.Tier0Config import setInjectRuns

# Create the Tier0 configuration object
tier0Config = createTier0Config()

# Set the verstion configuration (not used at the moment)
setConfigVersion(tier0Config, "replace with real version")

# Set run number to replay
setInjectRuns(tier0Config, [ 999999 ])

# Settings up sites
processingSite = "T0_CH_CERN"

# Set global parameters:
#  Acquisition era
#  BaseRequestPriority
#  Backfill mode
#  Data type
#  Processing site (where jobs run)
#  PhEDEx locations
setAcquisitionEra(tier0Config, "Tier0_REPLAY_vocms229")
setBaseRequestPriority(tier0Config, 300000)
setBackfill(tier0Config, 1)
setBulkDataType(tier0Config, "data")
setProcessingSite(tier0Config, processingSite)

# Override for DQM data tier
setDQMDataTier(tier0Config, "DQMIO")

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
                           alcaHarvestDir = "/store/unmerged/tier0_harvest",
                           conditionUploadTimeout = 18*3600,
                           dropboxHost = "webcondvm.cern.ch",
                           validationMode = True)

# Defaults for CMSSW version
defaultCMSSWVersion = "CMSSW_9_2_10"

# Configure ScramArch
setDefaultScramArch(tier0Config, "slc6_amd64_gcc530")
setScramArch(tier0Config, "CMSSW_5_3_20", "slc6_amd64_gcc472")

# Configure scenarios
ppScenario = "pp"
cosmicsScenario = "cosmics"
hcalnzsScenario = "hcalnzs"

# Defaults for processing version
defaultProcVersion = 1
expressProcVersion = 1
alcarawProcVersion = 1

# Defaults for GlobalTag
expressGlobalTag = "92X_dataRun2_Express_v7"
promptrecoGlobalTag = "92X_dataRun2_Prompt_v8"
alcap0GlobalTag = "92X_dataRun2_Prompt_v8"

# Mandatory for CondDBv2
globalTagConnect = "frontier://PromptProd/CMS_CONDITIONS"

# Multicore settings
numberOfCores = 4

# Splitting parameters for PromptReco
defaultRecoSplitting = 750 * numberOfCores
hiRecoSplitting = 200 * numberOfCores
alcarawSplitting = 20000 * numberOfCores

#
# Setup repack and express mappings
#
repackVersionOverride = {
    "CMSSW_5_2_7" : "CMSSW_5_3_20",
    "CMSSW_5_2_8" : "CMSSW_5_3_20",
    "CMSSW_5_2_9" : "CMSSW_5_3_20"
    }
expressVersionOverride = {
    "CMSSW_5_2_7" : "CMSSW_5_3_20",
    "CMSSW_5_2_8" : "CMSSW_5_3_20",
    "CMSSW_5_2_9" : "CMSSW_5_3_20"
    }

#set default repack settings for bulk streams
addRepackConfig(tier0Config, "Default",
                proc_ver = defaultProcVersion,
                maxSizeSingleLumi = 10 * 1024 * 1024 * 1024,
                maxSizeMultiLumi = 8 * 1024 * 1024 * 1024,
                minInputSize =  2.1 * 1024 * 1024 * 1024,
                maxInputSize = 4 * 1024 * 1024 * 1024,
                maxEdmSize = 10 * 1024 * 1024 * 1024,
                maxOverSize = 8 * 1024 * 1024 * 1024,
                maxInputEvents = 3 * 1000 * 1000,
                maxInputFiles = 1000,
                maxLatency = 24 * 3600,
                blockCloseDelay = 1200,
                versionOverride = repackVersionOverride)

addDataset(tier0Config, "Default",
           do_reco = False,
           write_reco = True, write_aod = True, write_miniaod = True, write_dqm = True,
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

###############################
### PDs used during Run2012 ###
###############################

# special scouting PD for parked data
addDataset(tier0Config, "DataScouting",
           do_reco = True,
           write_reco = False, write_aod = False, write_miniaod = False, write_dqm = True,
           reco_split = 10 * defaultRecoSplitting,
           scenario = "DataScouting")

addDataset(tier0Config, "Cosmics",
           do_reco = True,
           write_reco = True, write_aod = True, write_miniaod = False, write_dqm = True,
#           tape_node = "T1_US_FNAL_MSS",
#           disk_node = "T1_US_FNAL_Disk",
#           siteWhitelist = [ "T1_US_FNAL_Disk" ],
           timePerEvent = 0.5,
           sizePerEvent = 155,
           scenario = cosmicsScenario)
addDataset(tier0Config, "JetHT",
           do_reco = True,
           scenario = ppScenario)
addDataset(tier0Config, "MET",
           do_reco = True,
           scenario = ppScenario)
addDataset(tier0Config, "SingleMu",
           do_reco = True,
           scenario = ppScenario)
addDataset(tier0Config, "DoubleMu",
           do_reco = True,
           scenario = ppScenario)
addDataset(tier0Config, "MuOnia",
           do_reco = True,
           scenario = ppScenario)
addDataset(tier0Config, "SinglePhoton",
           do_reco = True,
           scenario = ppScenario)
addDataset(tier0Config, "DoublePhoton",
           do_reco = True,
           scenario = ppScenario)
addDataset(tier0Config, "DoublePhotonHighPt",
           do_reco = True,
           scenario = ppScenario)
addDataset(tier0Config, "SingleElectron",
           do_reco = True,
           scenario = ppScenario)
addDataset(tier0Config, "DoubleElectron",
           do_reco = True,
           scenario = ppScenario)
addDataset(tier0Config, "Commissioning",
           do_reco = True,
           scenario = ppScenario)
addDataset(tier0Config, "ParkingMonitor",
           do_reco = True,
           scenario = ppScenario)

datasets = [ "BJetPlusX", "BTag", "MultiJet", "MuEG", "MuHad", "ElectronHad",
             "PhotonHad", "HTMHT", "Tau", "TauPlusX", "NoBPTX", "JetMon" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenario)

datasets = [ "MinimumBias", "MinimumBias1", "MinimumBias2" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenario)

datasets = [ "L1Accept", "HcalHPDNoise", "LogMonitor", "RPCMonitor", "FEDMonitor" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False)

########################
### special test PDs ###
########################

addDataset(tier0Config, "HcalNZS",
           do_reco = True,
           scenario = hcalnzsScenario)
addDataset(tier0Config, "TestEnablesEcalHcalDT",
           do_reco = False,
           scenario = "AlCaTestEnable")
addDataset(tier0Config, "TestEnablesTracker",
           do_reco = True,
           write_reco = False, write_aod = False, write_miniaod = False, write_dqm = True,
           scenario = "AlCaTestEnable")

###########################
### special AlcaRaw PDs ###
###########################

addDataset(tier0Config, "AlCaP0",
           do_reco = False,
           write_reco = False, write_aod = False, write_miniaod = False, write_dqm = True,
           reco_split = alcarawSplitting,
           proc_version = alcarawProcVersion,
           global_tag = alcap0GlobalTag,
           scenario = "AlCaP0")
addDataset(tier0Config, "AlCaPhiSym",
           do_reco = False,
           write_reco = False, write_aod = False, write_miniaod = False, write_dqm = True,
           reco_split = alcarawSplitting,
           proc_version = alcarawProcVersion,
           scenario = "AlCaPhiSymEcal")
addDataset(tier0Config, "AlCaLumiPixels",
           do_reco = True,
           write_reco = False, write_aod = False, write_miniaod = False, write_dqm = True,
           reco_split = alcarawSplitting,
           proc_version = alcarawProcVersion,
           timePerEvent = 0.02,
           sizePerEvent = 38,
           scenario = "AlCaLumiPixels")


#############################
### Parking PDs from 7e33 ###
#############################

datasets = [ "DoubleMuParked", "HTMHTParked", "MuOniaParked",
             "MultiJet1Parked", "TauParked", "VBF1Parked" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False)


################################
### Parked PDs from Run2012D ###
################################

datasets = [ "SinglePhotonParked", "METParked", "HLTPhysicsParked", "ZeroBiasParked" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False)


#######################################
### Low-Pileup fill PDs / TOTEM Run ###
#######################################

datasets = [ "LP_L1Jets", "LP_ExclEGMU", "LP_Jets1", "LP_Jets2", "LP_MinBias1", "LP_MinBias2",
             "LP_MinBias3", "LP_RomanPots", "LP_ZeroBias", "LP_Central", "LP_Forward" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenario)


############################
### HI proton-lead tests ###
############################

datasets = [ "PAPhysics", "PAZeroBias1", "PAZeroBias2", ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               reco_split = hiRecoSplitting,
               scenario = ppScenario)


###############################
### Heavy Ion 2013 datasets ###
###############################

addDataset(tier0Config, "PAMinBiasUPC",
           do_reco = True,
           reco_split = hiRecoSplitting,
           scenario = ppScenario)

addDataset(tier0Config, "PAMuon",
           do_reco = True,
           reco_split = hiRecoSplitting,
           scenario = ppScenario)

datasets = [ "PAHighPt", "PAMinBias1", "PAMinBias2" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               reco_split = hiRecoSplitting,
               scenario = ppScenario)


########################################################
### ZeroBias PDs - extra ones used for various tests ###
########################################################

datasets = [ "ZeroBias", "ZeroBias1", "ZeroBias2", "ZeroBias3", "ZeroBias4",
             "ZeroBias5", "ZeroBias6", "ZeroBias7", "ZeroBias8", "ZeroBiasVdm" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenario)

#################################
### PDs used for High PU runs ###
#################################

datasets = [ "HighPileUpHPF", "L1EGHPF", "L1MuHPF", "L1JetHPF",
             "ZeroBiasHPF0", "HLTPhysics1", "HLTPhysics2" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenario)


#####################
### 25ns datasets ###
#####################

addDataset(tier0Config, "Cosmics25ns",
           do_reco = True,
           write_reco = True, write_aod = True, write_miniaod = False, write_dqm = True,
           scenario = cosmicsScenario)
addDataset(tier0Config, "DoubleElectron25ns",
           do_reco = True,
           scenario = ppScenario)
addDataset(tier0Config, "DoubleMu25ns",
           do_reco = True,
           scenario = ppScenario)
addDataset(tier0Config, "DoubleMuParked25ns",
           do_reco = True,
           scenario = ppScenario)
addDataset(tier0Config, "HcalNZS25ns",
           do_reco = True,
           scenario = hcalnzsScenario)
addDataset(tier0Config, "MinimumBias25ns",
           do_reco = True,
           scenario = ppScenario)
addDataset(tier0Config, "SingleMu25ns",
           do_reco = True,
           scenario = ppScenario)

datasets = [ "BJetPlusX25ns", "BTag25ns", "Commissioning25ns", "DoublePhoton25ns", "DoublePhotonHighPt25ns",
             "ElectronHad25ns", "HLTPhysics25ns1", "HLTPhysics25ns2", "HLTPhysics25ns3", "HLTPhysics25ns4",
             "HTMHT25ns", "HTMHTParked25ns", "VBF1Parked25ns", "JetHT25ns", "JetMon25ns", "MET25ns",
             "METParked25ns", "MuEG25ns", "MuHad25ns", "MuOnia25ns", "MuOniaParked25ns", "MultiJet25ns",
             "NoBPTX25ns", "MultiJet1Parked25ns", "ParkingMonitor25ns", "PhotonHad25ns", "SingleElectron25ns",
             "SinglePhoton25ns", "SinglePhotonParked25ns", "Tau25ns", "TauParked25ns", "TauPlusX25ns",
             "ZeroBias25ns1", "ZeroBias25ns2", "ZeroBias25ns3", "ZeroBias25ns4", "ZeroBias25ns5",
             "ZeroBias25ns6", "ZeroBias25ns7", "ZeroBias25ns8" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenario)

datasets = [ "HcalHPDNoise25ns", "LogMonitor25ns", "FEDMonitor25ns" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False)


#############################
### Express configuration ###
#############################

addExpressConfig(tier0Config, "HIExpress",
                 scenario = "HeavyIons",
                 data_tiers = [ "FEVT" ],
                 write_dqm = True,
                 reco_version = defaultCMSSWVersion,
                 multicore = numberOfCores,
                 global_tag = expressGlobalTag,
                 global_tag_connect = globalTagConnect,
                 proc_ver = expressProcVersion,
                 maxInputRate = 23 * 1000,
                 maxInputEvents = 23 * 1000,
                 maxInputSize = 2 * 1024 * 1024 * 1024,
                 maxInputFiles = 20,
                 maxLatency = 15 * 23,
                 periodicHarvestInterval = 20 * 60,
                 blockCloseDelay = 1200,
                 timePerEvent = 4,
                 sizePerEvent = 1700,
                 versionOverride = expressVersionOverride)

addExpressConfig(tier0Config, "Express",
                 scenario = ppScenario,
                 data_tiers = [ "FEVT" ],
                 write_dqm = True,
                 reco_version = defaultCMSSWVersion,
                 multicore = numberOfCores,
                 global_tag = expressGlobalTag,
                 global_tag_connect = globalTagConnect,
                 proc_ver = expressProcVersion,
                 maxInputRate = 23 * 1000,
                 maxInputEvents = 23 * 1000,
                 maxInputSize = 2 * 1024 * 1024 * 1024,
                 maxInputFiles = 20,
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
                 reco_version = defaultCMSSWVersion,
                 multicore = numberOfCores,
                 global_tag = expressGlobalTag,
                 global_tag_connect = globalTagConnect,
                 proc_ver = expressProcVersion,
                 maxInputRate = 23 * 1000,
                 maxInputEvents = 23 * 1000,
                 maxInputSize = 2 * 1024 * 1024 * 1024,
                 maxInputFiles = 20,
                 maxLatency = 15 * 23,
                 periodicHarvestInterval = 20 * 60,
                 blockCloseDelay = 1200,
                 timePerEvent = 4,
                 sizePerEvent = 1700,
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

###################################
### currently inactive settings ###
###################################

##addRegistrationConfig(tier0Config, "UserStreamExample1",
##                      primds = "ExamplePrimDS1",
##                      acq_era = "AcqEra1",
##                      proc_string = "OptionalProcString",
##                      proc_version = "v1",
##                      data_tier = "RAW")

##addConversionConfig(tier0Config, "UserStreamExample",
##                    primds = "PrimDSTest6",
##                    acq_era = "AquEraTest6",
##                    proc_string = "ProcStringTest6",
##                    proc_version = "v6",
##                    data_tier = "RAW",
##                    conv_type = "streamer")

if __name__ == '__main__':
    print(tier0Config)
