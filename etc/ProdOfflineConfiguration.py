"""
_OfflineConfiguration_

Processing configuration for the Tier0 - Production version
"""

from T0.RunConfig.Tier0Config import addDataset
from T0.RunConfig.Tier0Config import createTier0Config
from T0.RunConfig.Tier0Config import setAcquisitionEra
from T0.RunConfig.Tier0Config import setScramArch
from T0.RunConfig.Tier0Config import setDefaultScramArch
from T0.RunConfig.Tier0Config import setBaseRequestPriority
from T0.RunConfig.Tier0Config import setBackfill
from T0.RunConfig.Tier0Config import setBulkDataType
from T0.RunConfig.Tier0Config import setProcessingSite
from T0.RunConfig.Tier0Config import setBulkInjectNode
from T0.RunConfig.Tier0Config import setExpressInjectNode
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
#processingSite = "T2_CH_CERN_T0"
#cernPhedexNode = "T2_CH_CERN"
processingSite = "T2_CH_CERN_AI"
cernPhedexNode = "T0_CH_CERN_Disk"


# Set global parameters:
#  Acquisition era
#  BaseRequestPriority
#  Backfill mode
#  Data type
#  Processing site (where jobs run)
#  PhEDEx locations
setAcquisitionEra(tier0Config, "Run2015D")
setBaseRequestPriority(tier0Config, 250000)
setBackfill(tier0Config, None)
setBulkDataType(tier0Config, "data")
setProcessingSite(tier0Config, processingSite)
setBulkInjectNode(tier0Config, cernPhedexNode)
setExpressInjectNode(tier0Config, cernPhedexNode)
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


# Defaults for CMSSW version
defaultCMSSWVersion = "CMSSW_7_4_12_patch4"

# Configure ScramArch
setDefaultScramArch(tier0Config, "slc6_amd64_gcc491")

# Configure scenarios
ppScenario = "ppRun2"
ppScenarioB0T = "ppRun2"
cosmicsScenario = "cosmicsRun2"
hcalnzsScenario = "hcalnzsRun2"

# Defaults for processing version
defaultProcVersionRAW = 1
defaultProcVersionReco = 3
expressProcVersion = 3
alcarawProcVersion = 3

# Defaults for GlobalTag
expressGlobalTag = "74X_dataRun2_Express_v2"
promptrecoGlobalTag = "74X_dataRun2_Prompt_v2"
alcap0GlobalTag = "74X_dataRun2_Prompt_v2"

globalTagConnect = "frontier://PromptProd/CMS_CONDITIONS"

# Multicore settings
numberOfCores = 4

# Splitting parameters for PromptReco
defaultRecoSplitting = 2000 * numberOfCores
hiRecoSplitting = 200 * numberOfCores
alcarawSplitting = 20000 * numberOfCores

#
# Setup repack and express mappings
#
repackVersionOverride = {
    "CMSSW_7_4_2" : "CMSSW_7_4_12_patch4",
    "CMSSW_7_4_3" : "CMSSW_7_4_12_patch4",
    "CMSSW_7_4_4" : "CMSSW_7_4_12_patch4",
    "CMSSW_7_4_5" : "CMSSW_7_4_12_patch4",
    "CMSSW_7_4_6" : "CMSSW_7_4_12_patch4",
    "CMSSW_7_4_7" : "CMSSW_7_4_12_patch4",
    "CMSSW_7_4_8" : "CMSSW_7_4_12_patch4",
    "CMSSW_7_4_9" : "CMSSW_7_4_12_patch4",
    "CMSSW_7_4_10" : "CMSSW_7_4_12_patch4",
    "CMSSW_7_4_11" : "CMSSW_7_4_12_patch4",
    "CMSSW_7_4_12" : "CMSSW_7_4_12_patch4",
    }
expressVersionOverride = {
    "CMSSW_7_4_2" : "CMSSW_7_4_12_patch4",
    "CMSSW_7_4_3" : "CMSSW_7_4_12_patch4",
    "CMSSW_7_4_4" : "CMSSW_7_4_12_patch4",
    "CMSSW_7_4_5" : "CMSSW_7_4_12_patch4",
    "CMSSW_7_4_6" : "CMSSW_7_4_12_patch4",
    "CMSSW_7_4_7" : "CMSSW_7_4_12_patch4",
    "CMSSW_7_4_8" : "CMSSW_7_4_12_patch4",
    "CMSSW_7_4_9" : "CMSSW_7_4_12_patch4",
    "CMSSW_7_4_10" : "CMSSW_7_4_12_patch4",
    "CMSSW_7_4_11" : "CMSSW_7_4_12_patch4",
    "CMSSW_7_4_12" : "CMSSW_7_4_12_patch4",
    }

#set default repack settings for bulk streams
addRepackConfig(tier0Config, "Default",
                proc_ver = defaultProcVersionRAW,
                maxSizeSingleLumi = 10 * 1024 * 1024 * 1024,
                maxSizeMultiLumi = 8 * 1024 * 1024 * 1024,
                minInputSize =  2.1 * 1024 * 1024 * 1024,
                maxInputSize = 4 * 1024 * 1024 * 1024,
                maxEdmSize = 10 * 1024 * 1024 * 1024,
                maxOverSize = 8 * 1024 * 1024 * 1024,
                maxInputEvents = 250 * 1000,
                maxInputFiles = 1000,
                blockCloseDelay = 24 * 3600,
                versionOverride = repackVersionOverride)

addDataset(tier0Config, "Default",
           do_reco = False,
           write_reco = True, write_aod = True, write_miniaod = True, write_dqm = False,
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
           blockCloseDelay = 24 * 3600,
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
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "NoBPTX_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "Jet", "EGamma" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenario)

datasets = [ "Jet_0T", "EGamma_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenarioB0T)

datasets = [ "MinimumBias" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               alca_producers = [ "SiStripCalZeroBias", "SiStripCalMinBias", "TkAlMinBias" ],
               scenario = ppScenario)

datasets = [ "MinimumBias_0T" ]

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
               scenario = ppScenario)

datasets = [ "L1TechBPTXPlusOnly_0T", "L1TechBPTXMinusOnly_0T", "L1TechBPTXQuiet_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
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

addDataset(tier0Config,"AlCaLumiPixels",
           do_reco = True,
           write_reco = False, write_aod = False, write_miniaod = False, write_dqm = True,
           reco_split = alcarawSplitting,
           proc_version = alcarawProcVersion,
           alca_producers = [ "LumiPixels" ],
           timePerEvent = 0.02,
           sizePerEvent = 38,
           scenario = "AlCaLumiPixels")

########################################################
### ZeroBias PDs                                     ###
########################################################

datasets = [ "ZeroBias1", "ZeroBias2", "ZeroBias3", "ZeroBias4",
             "ZeroBias5", "ZeroBias6", "ZeroBias7", "ZeroBias8",
             "ZeroBias"  ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "SiStripCalZeroBias", "TkAlMinBias", "LumiPixelsMinBias" ],
               dqm_sequences = [ "@commonSiStripZeroBias", "@ecal", "@hcal", "@muon" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               timePerEvent = 3.5,
               sizePerEvent = 1500,
               scenario = ppScenario)

datasets = [ "ZeroBias1_0T", "ZeroBias2_0T", "ZeroBias3_0T", "ZeroBias4_0T",
             "ZeroBias5_0T", "ZeroBias6_0T", "ZeroBias7_0T", "ZeroBias8_0T",
             "ZeroBias_0T"  ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               alca_producers = [ "SiStripCalZeroBias", "TkAlMinBias", "LumiPixelsMinBias" ],
               dqm_sequences = [ "@commonSiStripZeroBias", "@ecal", "@hcal", "@muon" ],
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
               dqm_sequences = [ "@common" ],
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
               dqm_sequences = [ "@common" ],
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
               scenario = ppScenario)

datasets = [ "CastorJets_0T", "EGMLowPU_0T", "EmptyBX_0T", "FSQJets1_0T", "FSQJets2_0T", "FSQJets3_0T",
             "FullTrack_0T", "HINCaloJet40_0T", "HINCaloJets_0T", "HINCaloJetsOther_0T", "HINMuon_0T", 
             "HINPFJets_0T", "HINPFJetsOther_0T", "HINPhoton_0T", "HighMultiplicity85_0T", "L1MinimumBias_0T",
             "L1MinimumBiasHF1_0T", "L1MinimumBiasHF2_0T", "L1MinimumBiasHF3_0T", "L1MinimumBiasHF4_0T",
             "L1MinimumBiasHF5_0T", "L1MinimumBiasHF6_0T", "L1MinimumBiasHF7_0T", "L1MinimumBiasHF8_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenarioB0T)

datasets = [ "HcalHPDNoise" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "HcalHPDNoise_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

################################
### Special Totem runs       ###
################################

datasets = [ "TOTEM_minBias", "TOTEM_romanPots", "ToTOTEM", "ZeroBiasTotem", "MinimumBiasTotem",
             "TOTEM_minBias1", "TOTEM_minBias2", "TOTEM_romanPots1", "TOTEM_romanPots2", "TOTEM_romanPots3" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenario)

datasets = [ "TOTEM_minBias_0T", "TOTEM_romanPots_0T", "ToTOTEM_0T", "ZeroBiasTotem_0T", "MinimumBiasTotem_0T",
             "TOTEM_minBias1_0T", "TOTEM_minBias2_0T", "TOTEM_romanPots1_0T", "TOTEM_romanPots2_0T", 'TOTEM_romanPots3_0T'  ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenarioB0T)

################################
### 50 ns Physics Menu       ###
################################

datasets = [ "BTagCSV", "DisplacedJet" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               tape_node = "T1_ES_PIC_MSS",
               disk_node = "T1_ES_PIC_Disk",
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "BTagCSV_0T", "DisplacedJet_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               tape_node = "T1_ES_PIC_MSS",
               disk_node = "T1_ES_PIC_Disk",
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "MuonEG" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               tape_node = "T1_FR_CCIN2P3_MSS",
               disk_node = "T1_FR_CCIN2P3_Disk",
               physics_skims = [ "TopMuEG", "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "MuonEG_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               tape_node = "T1_FR_CCIN2P3_MSS",
               disk_node = "T1_FR_CCIN2P3_Disk",
               physics_skims = [ "TopMuEG", "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "DoubleMuonLowMass" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               tape_node = "T1_FR_CCIN2P3_MSS",
               disk_node = "T1_FR_CCIN2P3_Disk",
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "DoubleMuonLowMass_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               tape_node = "T1_FR_CCIN2P3_MSS",
               disk_node = "T1_FR_CCIN2P3_Disk",
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "HTMHT" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
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
               tape_node = "T1_US_FNAL_MSS",
               disk_node = "T1_US_FNAL_Disk",
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "Tau_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               tape_node = "T1_US_FNAL_MSS",
               disk_node = "T1_US_FNAL_Disk",
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "BTagMu" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               tape_node = "T1_IT_CNAF_MSS",
               disk_node = "T1_IT_CNAF_Disk",
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "BTagMu_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               tape_node = "T1_IT_CNAF_MSS",
               disk_node = "T1_IT_CNAF_Disk",
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "Charmonium" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               tape_node = "T1_DE_KIT_MSS",
               disk_node = "T1_DE_KIT_Disk",
               alca_producers = [ "TkAlJpsiMuMu" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "Charmonium_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               dqm_sequences = [ "@common" ],
               tape_node = "T1_DE_KIT_MSS",
               disk_node = "T1_DE_KIT_Disk",
               alca_producers = [ "TkAlJpsiMuMu" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "DoubleEG" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               tape_node = "T1_US_FNAL_MSS",
               disk_node = "T1_US_FNAL_Disk",
               alca_producers = [ "EcalCalZElectron", "EcalUncalZElectron", "HcalCalIterativePhiSym" ],
               dqm_sequences = [ "@common", "@ecal", "@egamma" ],
               physics_skims = [ "ZElectron", "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "DoubleEG_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               tape_node = "T1_US_FNAL_MSS",
               disk_node = "T1_US_FNAL_Disk",
               alca_producers = [ "EcalCalZElectron", "EcalUncalZElectron", "HcalCalIterativePhiSym" ],
               dqm_sequences = [ "@common", "@ecal", "@egamma" ],
               physics_skims = [ "ZElectron", "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "SingleMu" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenario)

datasets = [ "SingleMu_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenarioB0T)

datasets = [ "SingleMuon" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               tape_node = "T1_US_FNAL_MSS",
               disk_node = "T1_US_FNAL_Disk",
               alca_producers = [ "TkAlMuonIsolated", "HcalCalIterativePhiSym", "DtCalib", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu" ],
               dqm_sequences = [ "@common", "@muon" ],
               physics_skims = [ "ZMu", "MuTau", "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "SingleMuon_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               tape_node = "T1_US_FNAL_MSS",
               disk_node = "T1_US_FNAL_Disk",
               alca_producers = [ "TkAlMuonIsolated", "HcalCalIterativePhiSym", "DtCalib", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu" ],
               dqm_sequences = [ "@common", "@muon" ],
               physics_skims = [ "ZMu", "MuTau", "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "DoubleMu" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenario)

datasets = [ "DoubleMu_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenarioB0T)

datasets = [ "DoubleMuon" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               tape_node = "T1_ES_PIC_MSS",
               disk_node = "T1_ES_PIC_Disk",
               alca_producers = [ "TkAlZMuMu", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu", "DtCalib" ],
               dqm_sequences = [ "@common", "@muon" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "DoubleMuon_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               tape_node = "T1_ES_PIC_MSS",
               disk_node = "T1_ES_PIC_Disk",
               alca_producers = [ "TkAlZMuMu", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu", "DtCalib" ],
               dqm_sequences = [ "@common", "@muon" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "JetHT" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               tape_node = "T1_IT_CNAF_MSS",
               disk_node = "T1_IT_CNAF_Disk",
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
               tape_node = "T1_IT_CNAF_MSS",
               disk_node = "T1_IT_CNAF_Disk",
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
               tape_node = "T1_FR_CCIN2P3_MSS",
               disk_node = "T1_FR_CCIN2P3_Disk",
               alca_producers = [ "HcalCalNoise" ],
               dqm_sequences = [ "@common", "@jetmet", "@hcal" ],
               physics_skims = [ "HighMET", "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "MET_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               tape_node = "T1_FR_CCIN2P3_MSS",
               disk_node = "T1_FR_CCIN2P3_Disk",
               alca_producers = [ "HcalCalNoise" ],
               dqm_sequences = [ "@common", "@jetmet", "@hcal" ],
               physics_skims = [ "HighMET", "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "MuOnia" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               tape_node = "T1_UK_RAL_MSS",
               disk_node = "T1_UK_RAL_Disk",
               alca_producers = [ "TkAlUpsilonMuMu" ],
               dqm_sequences = [ "@common", "@muon" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "MuOnia_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               tape_node = "T1_UK_RAL_MSS",
               disk_node = "T1_UK_RAL_Disk",
               alca_producers = [ "TkAlUpsilonMuMu" ],
               dqm_sequences = [ "@common", "@muon" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "SingleElectron" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               tape_node = "T1_US_FNAL_MSS",
               disk_node = "T1_US_FNAL_Disk",
               alca_producers = [ "EcalCalWElectron", "EcalUncalWElectron", "EcalCalZElectron", "EcalUncalZElectron", "HcalCalIterativePhiSym" ],
               dqm_sequences = [ "@common", "@ecal", "@egamma" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "SingleElectron_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               tape_node = "T1_US_FNAL_MSS",
               disk_node = "T1_US_FNAL_Disk",
               alca_producers = [ "EcalCalWElectron", "EcalUncalWElectron", "EcalCalZElectron", "EcalUncalZElectron", "HcalCalIterativePhiSym" ],
               dqm_sequences = [ "@common", "@ecal", "@egamma" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenarioB0T)

datasets = [ "TestEnablesEcalHcal" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               alca_producers = [ "HcalCalPedestal" ],
               scenario = ppScenario)

datasets = [ "TestEnablesEcalHcal_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               alca_producers = [ "HcalCalPedestal" ],
               scenario = ppScenarioB0T)

datasets = [ "SinglePhoton" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               tape_node = "T1_DE_KIT_MSS",
               disk_node = "T1_DE_KIT_Disk",
               alca_producers = [ "HcalCalGammaJet" ],
               dqm_sequences = [ "@common", "@ecal", "@egamma" ],
               physics_skims = [ "LogError", "LogErrorMonitor" ],
               scenario = ppScenario)

datasets = [ "SinglePhoton_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_dqm = True,
               tape_node = "T1_DE_KIT_MSS",
               disk_node = "T1_DE_KIT_Disk",
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
               scenario = ppScenario)

datasets = [ "HINPFJet100_0T", "HINCaloJet100_0T", "HighMultiplicity_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenarioB0T)

datasets = [ "HLTPhysicsCosmics", "HLTPhysicsCosmics1", "HLTPhysicsCosmics2",
            "HLTPhysicsCosmics3", "HLTPhysicsCosmics4", "HLTPhysicsCosmics5",
            "HLTPhysicsCosmics6", "HLTPhysicsCosmics7", "HLTPhysicsCosmics8" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_miniaod = False,
               scenario = cosmicsScenario)

datasets = [ "ParkingMonitor", "ParkingScoutingMonitor" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = False, write_aod = False, write_miniaod = True, write_dqm = True,
               tape_node = "T1_US_FNAL_MSS",
               disk_node = "T1_US_FNAL_Disk",
               scenario = ppScenario)

datasets = [ "ParkingMonitor_0T", "ParkingScoutingMonitor_0T" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               write_reco = False, write_aod = False, write_miniaod = True, write_dqm = True,
               tape_node = "T1_US_FNAL_MSS",
               disk_node = "T1_US_FNAL_Disk",
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
                                    "PromptCalibProdSiStrip", "PromptCalibProdSiStripGains" ],
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
                                    "PromptCalibProdSiStrip", "PromptCalibProdSiStripGains" ],
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
    print tier0Config
