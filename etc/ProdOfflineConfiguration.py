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
processingSite = "T2_CH_CERN_T0"
cernPhedexNode = "T2_CH_CERN"
#processingSite = "T2_CH_CERN_AI"
#cernPhedexNode = "T0_CH_CERN_Disk"


# Set global parameters:
#  Acquisition era
#  BaseRequestPriority
#  Backfill mode
#  Data type
#  Processing site (where jobs run)
#  PhEDEx locations
setAcquisitionEra(tier0Config, "Run2015B")
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
setDQMUploadUrl(tier0Config, "https://cmsweb.cern.ch/dqm/offline;https://cmsweb-testbed.cern.ch/dqm/offline")

# PCL parameters
setPromptCalibrationConfig(tier0Config,
                           alcaHarvestTimeout = 12*3600,
                           alcaHarvestDir = "/store/express/tier0_harvest",
                           conditionUploadTimeout = 18*3600,
                           dropboxHost = "webcondvm.cern.ch",
                           validationMode = False)


# Defaults for CMSSW version
defaultCMSSWVersion = "CMSSW_7_4_7"

# Configure ScramArch
setDefaultScramArch(tier0Config, "slc6_amd64_gcc491")

# Configure scenarios
cosmicsScenario = "cosmicsRun2"
ppScenario = "ppRun2"
hcalnzsScenario = "hcalnzsRun2"

# Defaults for processing version
defaultProcVersionRAW = 1
defaultProcVersionReco = 1
expressProcVersion = 1
alcarawProcVersion = 1

# Defaults for GlobalTag
expressGlobalTag = "74X_dataRun2_Express_v0"
promptrecoGlobalTag = "74X_dataRun2_Prompt_v0"
alcap0GlobalTag = "74X_dataRun2_Prompt_v0"

globalTagConnect = "frontier://PromptProd/CMS_CONDITIONS"

# Multicore settings
numberOfCores = 1

# Splitting parameters for PromptReco
defaultRecoSplitting = 2000 * numberOfCores
hiRecoSplitting = 200 * numberOfCores
alcarawSplitting = 20000 * numberOfCores

#
# Setup repack and express mappings
#
repackVersionOverride = {
    "CMSSW_7_4_2" : "CMSSW_7_4_7",
    "CMSSW_7_4_3" : "CMSSW_7_4_7",
    "CMSSW_7_4_4" : "CMSSW_7_4_7",
    "CMSSW_7_4_5" : "CMSSW_7_4_7",
    "CMSSW_7_4_6" : "CMSSW_7_4_7",
    }
expressVersionOverride = {
    "CMSSW_7_4_2" : "CMSSW_7_4_7",
    "CMSSW_7_4_3" : "CMSSW_7_4_7",
    "CMSSW_7_4_4" : "CMSSW_7_4_7",
    "CMSSW_7_4_5" : "CMSSW_7_4_7",
    "CMSSW_7_4_6" : "CMSSW_7_4_7",
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
           write_reco = True, write_aod = True, write_miniaod = True, write_dqm = True,
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
           scenario = ppScenario)

###############################
### PDs used during Run2015 ###
###############################

addDataset(tier0Config, "Cosmics",
           do_reco = True,
           write_reco = True, write_aod = True, write_miniaod = False, write_dqm = True,
           alca_producers = [ "TkAlCosmics0T", "MuAlGlobalCosmics", "HcalCalHOCosmics", "DtCalibCosmics" ],
           scenario = cosmicsScenario)

addDataset(tier0Config, "Commissioning",
           do_reco = True,
           alca_producers = [ "TkAlMinBias", "SiStripCalMinBias" ],
           scenario = ppScenario)

datasets = [ "NoBPTX" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenario)

datasets = [ "Jet", "EGamma" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenario)

datasets = [ "MinimumBias" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               alca_producers = [ "SiStripCalZeroBias", "SiStripCalMinBias", "TkAlMinBias" ],
               scenario = ppScenario)

datasets = [ "L1TechBPTXPlusOnly", "L1TechBPTXMinusOnly", "L1TechBPTXQuiet" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenario)

########################
### special test PDs ###
########################

addDataset(tier0Config, "HcalNZS",
           do_reco = True,
           alca_producers = [ "HcalCalMinBias" ],
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
               alca_producers = [ "SiStripCalZeroBias", "TkAlMinBias", "LumiPixelsMinBias" ],
               scenario = ppScenario)

########################################################
### HLTPhysics PDs                                   ###
########################################################

datasets = [ "HLTPhysics1", "HLTPhysics2", "HLTPhysics3", "HLTPhysics4",
             "HLTPhysics5", "HLTPhysics6", "HLTPhysics7", "HLTPhysics8",
             "HLTPhysics"  ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               alca_producers = [ "SiStripCalMinBias", "TkAlMinBias" ],
               scenario = ppScenario)

################################
### Low PU collisions 13 TeV ###
################################

datasets = [ "CastorJets", "EGMLowPU", "EmptyBX", "FSQJets1", "FSQJets2", "FSQJets3", 
             "FullTrack", "HINCaloJet40", "HINCaloJetsOther", "HINMuon", "HINPFJetsOther", 
             "HINPhoton", "HcalHPDNoise", "HighMultiplicity", "L1MinimumBias",
             "L1MinimumBiasHF1", "L1MinimumBiasHF2", "L1MinimumBiasHF3", "L1MinimumBiasHF4",
             "L1MinimumBiasHF5", "L1MinimumBiasHF6", "L1MinimumBiasHF7", "L1MinimumBiasHF8" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenario)

################################
### Special Totem runs       ###
################################

datasets = [ "TOTEMMinBias", "TOTEMRomanPots", "ToTOTEM", "ZeroBiasTotem", "MinimumBiasTotem"  ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenario)

################################
### 50 ns Physics Menu       ###
################################

datasets = [ "BTagCSV", "BTagMu", "DisplacedJet", "DoubleMuonLowMass",
             "HTMHT", "MuonEG", "Tau" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenario)

datasets = [ "Charmonium" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               alca_producers = [ "TkAlJpsiMuMu" ],
               scenario = ppScenario)

datasets = [ "DoubleEG" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               alca_producers = [ "EcalCalZElectron", "EcalUncalZElectron", "HcalCalIterativePhiSym" ],
               scenario = ppScenario)

datasets = [ "SingleMu" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               alca_producers = [ "TkAlMuonIsolated", "HcalCalIterativePhiSym", "DtCalib", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu" ],
               scenario = ppScenario)

datasets = [ "SingleMuon" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               alca_producers = [ "TkAlMuonIsolated", "HcalCalIterativePhiSym", "DtCalib", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu" ],
               scenario = ppScenario)

datasets = [ "DoubleMu" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               alca_producers = [ "TkAlZMuMu", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu", "DtCalib" ],
               scenario = ppScenario)

datasets = [ "DoubleMuon" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               alca_producers = [ "TkAlZMuMu", "MuAlCalIsolatedMu", "MuAlOverlaps", "MuAlZMuMu", "DtCalib" ],
               scenario = ppScenario)

datasets = [ "JetHT" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               alca_producers = [ "HcalCalDijets" ],
               scenario = ppScenario)

datasets = [ "MET" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               alca_producers = [ "HcalCalNoise" ],
               scenario = ppScenario)

datasets = [ "MuOnia" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               alca_producers = [ "TkAlUpsilonMuMu" ],
               scenario = ppScenario)

datasets = [ "SingleElectron" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               alca_producers = [ "EcalCalWElectron", "EcalUncalWElectron", "EcalCalZElectron", "EcalUncalZElectron", "HcalCalIterativePhiSym" ],
               scenario = ppScenario)

datasets = [ "MuOnia" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               alca_producers = [ "HcalCalGammaJet" ],
               scenario = ppScenario)

datasets = [ "TestEnablesEcalHcal" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False,
               alca_producers = [ "HcalCalPedestals" ],
               scenario = ppScenario)

datasets = [ "SinglePhoton" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               alca_producers = [ "HcalCalGammaJet" ],
               scenario = ppScenario)

datasets = [ "HINPFJet100", "HINCaloJet100", "HighMultiplicity" ]

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
               scenario = cosmicsScenario)

#############################
### Express configuration ###
#############################

addExpressConfig(tier0Config, "Express",
                 scenario = ppScenario,
                 data_tiers = [ "FEVT" ],
                 write_dqm = True,
                 alca_producers = [ "SiStripPCLHistos", "SiStripCalZeroBias", "SiStripCalMinBias",
                                    "TkAlMinBias", "DtCalib", "PromptCalibProd", 
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
                 versionOverride = expressVersionOverride)

addExpressConfig(tier0Config, "ExpressCosmics",
                 scenario = cosmicsScenario,
                 data_tiers = [ "FEVT" ],
                 write_dqm = True,
                 alca_producers = [ "SiStripPCLHistos", "SiStripCalZeroBias", "TkAlCosmics0T", "PromptCalibProdSiStrip" ],
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
                 versionOverride = expressVersionOverride)

#######################
### ignored streams ###
#######################

ignoreStream(tier0Config, "Error")
ignoreStream(tier0Config, "HLTMON")
ignoreStream(tier0Config, "EventDisplay")
ignoreStream(tier0Config, "DQM")
ignoreStream(tier0Config, "LookArea")

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
