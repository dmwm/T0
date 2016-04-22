"""
_OfflineConfiguration_

Processing configuration for the Tier0 - Replay version
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
setAcquisitionEra(tier0Config, "Tier0_Test_SUPERBUNNIES_vocms229")
setBaseRequestPriority(tier0Config, 200000)
setBackfill(tier0Config, 1)
setBulkDataType(tier0Config, "data")
setProcessingSite(tier0Config, processingSite)
setExpressSubscribeNode(tier0Config, None)

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
defaultCMSSWVersion = "CMSSW_8_0_5"

# Configure ScramArch
setDefaultScramArch(tier0Config, "slc6_amd64_gcc491")
setScramArch(tier0Config, "CMSSW_8_0_0", "slc6_amd64_gcc493")
setScramArch(tier0Config, "CMSSW_8_0_0_patch1", "slc6_amd64_gcc493")
setScramArch(tier0Config, "CMSSW_8_0_0_patch2", "slc6_amd64_gcc493")
setScramArch(tier0Config, "CMSSW_8_0_0_patch3", "slc6_amd64_gcc493")
setScramArch(tier0Config, "CMSSW_8_0_1", "slc6_amd64_gcc493")
setScramArch(tier0Config, "CMSSW_8_0_2", "slc6_amd64_gcc493")
setScramArch(tier0Config, "CMSSW_8_0_3", "slc6_amd64_gcc493")
setScramArch(tier0Config, "CMSSW_8_0_3_patch1", "slc6_amd64_gcc493")
setScramArch(tier0Config, "CMSSW_8_0_4", "slc6_amd64_gcc493")
setScramArch(tier0Config, "CMSSW_8_0_5", "slc6_amd64_gcc493")

# Configure scenarios
#ppScenario = "ppEra_Run2_25ns"
#ppScenarioB0T = "ppEra_Run2_25ns"
#cosmicsScenario = "cosmicsEra_Run2_25ns"
#hcalnzsScenario = "hcalnzsEra_Run2_25ns" 

ppScenario = "ppEra_Run2_2016"
ppScenarioB0T = "ppEra_Run2_2016"
cosmicsScenario = "cosmicsEra_Run2_2016"
hcalnzsScenario = "hcalnzsEra_Run2_2016"

# Defaults for processing version
defaultProcVersion = 1
expressProcVersion = 1
alcarawProcVersion = 1

# Defaults for GlobalTag
expressGlobalTag = "80X_dataRun2_Express_v5"
promptrecoGlobalTag = "80X_dataRun2_Prompt_v6"
alcap0GlobalTag = "80X_dataRun2_Prompt_v6"

# Mandatory for CondDBv2
globalTagConnect = "frontier://PromptProd/CMS_CONDITIONS"

# Multicore settings
numberOfCores = 4

# Splitting parameters for PromptReco
defaultRecoSplitting = 1000 * numberOfCores
hiRecoSplitting = 100 * numberOfCores
alcarawSplitting = 10000 * numberOfCores

#
# Setup repack and express mappings
#
repackVersionOverride = {
    "CMSSW_7_5_8" : "CMSSW_7_5_8_patch3",
    "CMSSW_8_0_0" : "CMSSW_8_0_5",
    "CMSSW_8_0_1" : "CMSSW_8_0_5",
    "CMSSW_8_0_2" : "CMSSW_8_0_5",
    "CMSSW_8_0_3" : "CMSSW_8_0_5",
    "CMSSW_8_0_4" : "CMSSW_8_0_5",
    }

expressVersionOverride = {
    "CMSSW_7_5_8" : "CMSSW_7_5_8_patch3",
    "CMSSW_8_0_0" : "CMSSW_8_0_5",
    "CMSSW_8_0_1" : "CMSSW_8_0_5",
    "CMSSW_8_0_2" : "CMSSW_8_0_5",
    "CMSSW_8_0_3" : "CMSSW_8_0_5",
    "CMSSW_8_0_4" : "CMSSW_8_0_5"
    }

#set default repack settings for bulk streams
addRepackConfig(tier0Config, "Default",
                proc_ver = defaultProcVersion,
                maxSizeSingleLumi = 12 * 1024 * 1024 * 1024,
                maxSizeMultiLumi = 8 * 1024 * 1024 * 1024,
                minInputSize =  2.1 * 1024 * 1024 * 1024,
                maxInputSize = 4 * 1024 * 1024 * 1024,
                maxEdmSize = 12 * 1024 * 1024 * 1024,
                maxOverSize = 8 * 1024 * 1024 * 1024,
                maxInputEvents = 250 * 1000,
                maxInputFiles = 1000,
                maxLatency = 24 * 3600,
                blockCloseDelay = 1200,
                versionOverride = repackVersionOverride)

addDataset(tier0Config, "Default",
           do_reco = False,
           write_reco = True, write_aod = True, write_miniaod = True, write_dqm = False,
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
#           disk_node = "T1_CH_FNAL_Disk",
           blockCloseDelay = 1200,
           timePerEvent = 5,
           sizePerEvent = 1500,
           scenario = ppScenario)


###############################
### PDs used during Run2015 ###
###############################

addDataset(tier0Config, "Cosmics",
           do_reco = True,
           write_miniaod = False, write_dqm = True,
           alca_producers = [ "TkAlCosmics0T", "MuAlGlobalCosmics", "HcalCalHOCosmics", "DtCalibCosmics" ],
           physics_skims = [ "CosmicSP", "CosmicTP", "LogError", "LogErrorMonitor" ],
           timePerEvent = 0.5,
           sizePerEvent = 155,
           scenario = cosmicsScenario)

addDataset(tier0Config, "Commissioning",
           do_reco = True,
           write_dqm = True,
           alca_producers = [ "TkAlMinBias", "SiStripCalMinBias" ],
           dqm_sequences = [ "@common", "@hcal" ],
           physics_skims = [ "EcalActivity", "LogError", "LogErrorMonitor" ],
           timePerEvent = 12,
           sizePerEvent = 4000,
           scenario = ppScenario)

addDataset(tier0Config, "Commissioning_0T",
           do_reco = True,
           write_dqm = True,
           alca_producers = [ "TkAlMinBias", "SiStripCalMinBias" ],
           dqm_sequences = [ "@common", "@hcal" ],
           physics_skims = [ "EcalActivity", "LogError", "LogErrorMonitor" ],
           timePerEvent = 12,
           sizePerEvent = 4000,
           scenario = ppScenarioB0T)

datasets = [ "NoBPTX" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "NoBPTX_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
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

datasets = [ "MinimumBias1", "MinimumBias2", "MinimumBias3", "MinimumBias4",
             "MinimumBias5", "MinimumBias6", "MinimumBias7", "MinimumBias8",
             "MinimumBias9", "MinimumBias10", "MinimumBias11", "MinimumBias12",
             "MinimumBias13", "MinimumBias14", "MinimumBias15", "MinimumBias16",
             "MinimumBias17", "MinimumBias18", "MinimumBias19", "MinimumBias20",
             "MinimumBias" ]

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
             "MinimumBias17_0T", "MinimumBias18_0T", "MinimumBias19_0T", "MinimumBias20_0T",
             "MinimumBias_0T" ]

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
           dqm_sequences = [ "@common" ],
           alca_producers = [ "HcalCalMinBias" ],
           physics_skims = [ "LogError", "LogErrorMonitor" ],
           timePerEvent = 4.2,
           sizePerEvent = 1900,
           scenario = hcalnzsScenario)

addDataset(tier0Config, "HcalNZS_0T",
           do_reco = True,
           write_dqm = True,
           dqm_sequences = [ "@common" ],
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

datasets = [ "ZeroBias1", "ZeroBias2", "ZeroBias3", "ZeroBias4",
             "ZeroBias5", "ZeroBias6", "ZeroBias7", "ZeroBias8",
             "ZeroBias9", "ZeroBias10", "ZeroBias11", "ZeroBias12",
             "ZeroBias13", "ZeroBias14", "ZeroBias15", "ZeroBias16",
             "ZeroBias17", "ZeroBias18", "ZeroBias19", "ZeroBias20",
             "ZeroBias" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "SiStripCalZeroBias", "TkAlMinBias", "LumiPixelsMinBias" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               timePerEvent = 3.5,
               sizePerEvent = 1500,
               scenario = ppScenario)

datasets = [ "ZeroBias1_0T", "ZeroBias2_0T", "ZeroBias3_0T", "ZeroBias4_0T",
             "ZeroBias5_0T", "ZeroBias6_0T", "ZeroBias7_0T", "ZeroBias8_0T",
             "ZeroBias9_0T", "ZeroBias10_0T", "ZeroBias11_0T", "ZeroBias12_0T",
             "ZeroBias13_0T", "ZeroBias14_0T", "ZeroBias15_0T", "ZeroBias16_0T",
             "ZeroBias17_0T", "ZeroBias18_0T", "ZeroBias19_0T", "ZeroBias20_0T",
             "ZeroBias_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "SiStripCalZeroBias", "TkAlMinBias", "LumiPixelsMinBias" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               timePerEvent = 3.5,
               sizePerEvent = 1500,
               scenario = ppScenarioB0T)

########################################################
### HLTPhysics PDs                                   ###
########################################################

datasets = [ "HLTPhysics1", "HLTPhysics2", "HLTPhysics3", "HLTPhysics4",
             "HLTPhysics5", "HLTPhysics6", "HLTPhysics7", "HLTPhysics8",
             "HLTPhysics", "HLTPhysicspart0", "HLTPhysicspart1",
             "HLTPhysicspart2", "HLTPhysicspart3", "HLTPhysicspart4",
             "HLTPhysicspart5", "HLTPhysicspart6", "HLTPhysicspart7"  ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "SiStripCalMinBias", "TkAlMinBias" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "HLTPhysics1_0T", "HLTPhysics2_0T", "HLTPhysics3_0T", "HLTPhysics4_0T",
             "HLTPhysics5_0T", "HLTPhysics6_0T", "HLTPhysics7_0T", "HLTPhysics8_0T",
             "HLTPhysics_0T", "HLTPhysicspart0_0T", "HLTPhysicspart1_0T",
             "HLTPhysicspart2_0T", "HLTPhysicspart3_0T", "HLTPhysicspart4_0T",
             "HLTPhysicspart5_0T", "HLTPhysicspart6_0T", "HLTPhysicspart7_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "SiStripCalMinBias", "TkAlMinBias" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

################################
### Low PU collisions 13 TeV ###
################################

datasets = [ "CastorJets", "EGMLowPU", "EmptyBX", "FSQJets1", "FSQJets2", "FSQJets3", 
             "FullTrack", "HINCaloJet40", "HINCaloJets", "HINCaloJetsOther", "HINMuon", 
             "HINPFJets", "HINPFJetsOther", "HINPhoton", "HighMultiplicity85", "L1MinimumBias",
             "L1MinimumBiasHF1", "L1MinimumBiasHF2", "L1MinimumBiasHF3", "L1MinimumBiasHF4",
             "L1MinimumBiasHF5", "L1MinimumBiasHF6", "L1MinimumBiasHF7", "L1MinimumBiasHF8" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

datasets = [ "CastorJets_0T", "EGMLowPU_0T", "EmptyBX_0T", "FSQJets1_0T", "FSQJets2_0T", "FSQJets3_0T",
             "FullTrack_0T", "HINCaloJet40_0T", "HINCaloJets_0T", "HINCaloJetsOther_0T", "HINMuon_0T", 
             "HINPFJets_0T", "HINPFJetsOther_0T", "HINPhoton_0T", "HighMultiplicity85_0T", "L1MinimumBias_0T",
             "L1MinimumBiasHF1_0T", "L1MinimumBiasHF2_0T", "L1MinimumBiasHF3_0T", "L1MinimumBiasHF4_0T",
             "L1MinimumBiasHF5_0T", "L1MinimumBiasHF6_0T", "L1MinimumBiasHF7_0T", "L1MinimumBiasHF8_0T" ]

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

datasets = [ "BTagCSV", "DisplacedJet" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "BTagCSV_0T", "DisplacedJet_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "MuonEG" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "TopMuEG", "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "MuonEG_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "TopMuEG", "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "DoubleMuonLowMass" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "DoubleMuonLowMass_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "HTMHT" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               timePerEvent = 9.4,
               sizePerEvent = 2000,
               scenario = ppScenario)

datasets = [ "HTMHT_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               timePerEvent = 9.4,
               sizePerEvent = 2000,
               scenario = ppScenarioB0T)

datasets = [ "Tau" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "Tau_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "BTagMu" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "BTagMu_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "Charmonium" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               alca_producers = [ "TkAlJpsiMuMu" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "Charmonium_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               alca_producers = [ "TkAlJpsiMuMu" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "DoubleEG" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               alca_producers = [ "EcalCalZElectron", "EcalUncalZElectron", "HcalCalIterativePhiSym" ],
               dqm_sequences = [ "@common", "@ecal", "@egamma" ],
               physics_skims = [ "ZElectron", "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "DoubleEG_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "EcalCalZElectron", "EcalUncalZElectron", "HcalCalIterativePhiSym" ],
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
               write_dqm = True,
               alca_producers = [ "TkAlMuonIsolated", "HcalCalIterativePhiSym", "DtCalib", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu" ],
               dqm_sequences = [ "@common", "@muon" ],
               physics_skims = [ "ZMu", "MuTau", "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "SingleMuon_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "TkAlMuonIsolated", "HcalCalIterativePhiSym", "DtCalib", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu" ],
               dqm_sequences = [ "@common", "@muon" ],
               physics_skims = [ "ZMu", "MuTau", "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "DoubleMu" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
	       alca_producers = [ "TkAlZMuMu", "TkAlJpsiMuMu", "TkAlUpsilonMuMu", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu", "DtCalib" ],
               physics_skims = [ "Onia" ],
               scenario = ppScenario)

datasets = [ "DoubleMu_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               alca_producers = [ "TkAlZMuMu", "TkAlJpsiMuMu", "TkAlUpsilonMuMu", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu", "DtCalib" ],
               physics_skims = [ "Onia" ],
               scenario = ppScenarioB0T)

datasets = [ "DoubleMuon" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "TkAlZMuMu", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu", "DtCalib" ],
               dqm_sequences = [ "@common", "@muon" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "DoubleMuon_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "TkAlZMuMu", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu", "DtCalib" ],
               dqm_sequences = [ "@common", "@muon" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "JetHT" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "HcalCalDijets" ],
               dqm_sequences = [ "@common", "@jetmet", "@hcal" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               timePerEvent = 5.7,
               sizePerEvent = 2250,
               scenario = ppScenario)

datasets = [ "JetHT_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "HcalCalDijets" ],
               dqm_sequences = [ "@common", "@jetmet", "@hcal" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               timePerEvent = 5.7,
               sizePerEvent = 2250,
               scenario = ppScenarioB0T)

datasets = [ "MET" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "HcalCalNoise" ],
               dqm_sequences = [ "@common", "@jetmet", "@hcal" ],
               physics_skims = [ "HighMET", "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "MET_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "HcalCalNoise" ],
               dqm_sequences = [ "@common", "@jetmet", "@hcal" ],
               physics_skims = [ "HighMET", "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "MuOnia" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "TkAlUpsilonMuMu" ],
               dqm_sequences = [ "@common", "@muon" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "MuOnia_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "TkAlUpsilonMuMu" ],
               dqm_sequences = [ "@common", "@muon" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "SingleElectron" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "EcalCalWElectron", "EcalUncalWElectron", "EcalCalZElectron", "EcalUncalZElectron", "HcalCalIterativePhiSym" ],
               dqm_sequences = [ "@common", "@ecal", "@egamma" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "SingleElectron_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "EcalCalWElectron", "EcalUncalWElectron", "EcalCalZElectron", "EcalUncalZElectron", "HcalCalIterativePhiSym" ],
               dqm_sequences = [ "@common", "@ecal", "@egamma" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "TestEnablesEcalHcal" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               alca_producers = [ "HcalCalPedestal" ],
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

datasets = [ "TestEnablesEcalHcal_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               alca_producers = [ "HcalCalPedestal" ],
               dqm_sequences = [ "@common" ],
               scenario = ppScenarioB0T)

datasets = [ "SinglePhoton" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "HcalCalGammaJet" ],
               dqm_sequences = [ "@common", "@ecal", "@egamma" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "SinglePhoton_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
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

datasets = [ "HINPFJet100", "HINCaloJet100", "HighMultiplicity" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

datasets = [ "HINPFJet100_0T", "HINCaloJet100_0T", "HighMultiplicity_0T" ]

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
               write_miniaod = False,
               dqm_sequences = [ "@common" ],
               scenario = cosmicsScenario)

datasets = [ "ParkingMonitor", "ParkingScoutingMonitor" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = False, write_aod = False, write_miniaod = True, write_dqm = True,
               dqm_sequences = [ "@common" ],
               scenario = ppScenario)

datasets = [ "ParkingMonitor_0T", "ParkingScoutingMonitor_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = False, write_aod = False, write_miniaod = True, write_dqm = True,
               dqm_sequences = [ "@common" ],
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
           alca_producers = [ "TkAlMuonIsolated", "HcalCalIterativePhiSym", "DtCalib", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu" ],
           dqm_sequences = [ "@common" ],
           physics_skims = [ "ZMM" ],
           scenario = ppScenario)

addDataset(tier0Config, "SingleMuHighPt_0T",
           do_reco = True,
           write_dqm = True,
           alca_producers = [ "TkAlMuonIsolated", "HcalCalIterativePhiSym", "DtCalib", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu" ],
           dqm_sequences = [ "@common" ],
           physics_skims = [ "ZMM" ],
           scenario = ppScenarioB0T)

addDataset(tier0Config, "SingleMuLowPt",
           do_reco = True,
           write_dqm = True,
           alca_producers = [ "TkAlMuonIsolated", "HcalCalIterativePhiSym", "DtCalib", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu" ],
           dqm_sequences = [ "@common" ],
           scenario = ppScenario)

addDataset(tier0Config, "SingleMuLowPt_0T",
           do_reco = True,
           write_dqm = True,
           alca_producers = [ "TkAlMuonIsolated", "HcalCalIterativePhiSym", "DtCalib", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu" ],
           dqm_sequences = [ "@common" ],
           scenario = ppScenarioB0T)

#############################
### Express configuration ###
#############################

addExpressConfig(tier0Config, "Express",
                 scenario = ppScenario,
                 data_tiers = [ "FEVT" ],
                 write_dqm = True,
                 alca_producers = [ "SiStripPCLHistos", "SiStripCalZeroBias", "SiStripCalMinBias",
                                    "TkAlMinBias", "DtCalib", "PromptCalibProd", "Hotline",
                                    "PromptCalibProdSiStrip", "LumiPixelsMinBias" ],
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
                 alca_producers = [ "SiStripPCLHistos", "SiStripCalZeroBias", "SiStripCalMinBias",
                                    "TkAlMinBias", "DtCalib", "PromptCalibProd", "Hotline",
                                    "PromptCalibProdSiStrip", "LumiPixelsMinBias" ],
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

#######################
### ignored streams ###
#######################

ignoreStream(tier0Config, "Error")
ignoreStream(tier0Config, "HLTMON")
ignoreStream(tier0Config, "EventDisplay")
ignoreStream(tier0Config, "DQM")
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
