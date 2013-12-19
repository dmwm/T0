"""
_OfflineConfiguration_

Processing configuration for the Tier0 - Replay version
"""

from T0.RunConfig.Tier0Config import addDataset
from T0.RunConfig.Tier0Config import createTier0Config
from T0.RunConfig.Tier0Config import setAcquisitionEra
from T0.RunConfig.Tier0Config import setScramArch
from T0.RunConfig.Tier0Config import setDefaultScramArch
from T0.RunConfig.Tier0Config import setLFNPrefix
from T0.RunConfig.Tier0Config import setBulkDataType
from T0.RunConfig.Tier0Config import setBulkDataLocation
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

# Set global parameters:
#  Acquisition era
#  LFN prefix
#  Data type
#  PhEDEx location for Bulk data
setAcquisitionEra(tier0Config, "Tier0_Test_SUPERBUNNIES_vocms229")
setLFNPrefix(tier0Config, "/store/backfill/1")
setBulkDataType(tier0Config, "data")
setBulkDataLocation(tier0Config, "T2_CH_CERN")

# Define the two default timeouts for reco release
# First timeout is used directly for reco release
# Second timeout is used for the data service PromptReco start check
# (to basically say we started PromptReco even though we haven't)
defaultRecoTimeout =  600
defaultRecoLockTimeout = 60

# DQM Server
setDQMUploadUrl(tier0Config, "https://cmsweb.cern.ch/dqm/dev")

# PCL parameters
setPromptCalibrationConfig(tier0Config,
                           alcaHarvestTimeout = 12*3600,
                           alcaHarvestDir = "/afs/cern.ch/user/c/cmsprod/scratch2/tier0_harvest",
                           conditionUploadTimeout = 18*3600,
                           dropboxHost = "webcondvm.cern.ch",
                           validationMode = True)


# Defaults for CMSSW version
defaultCMSSWVersion = "CMSSW_6_2_4"

# Configure ScramArch
setDefaultScramArch(tier0Config, "slc5_amd64_gcc462")
setScramArch(tier0Config, "CMSSW_6_2_4", "slc5_amd64_gcc472")

# Defaults for processing version
defaultProcVersion = 1
expressProcVersion = 1
alcarawProcVersion = 1

# Defaults for GlobalTag 
promptrecoGlobalTag = "GR_R_62_V1::All"
#promptrecoGlobalTag = "GR_P_V43D::All"
expressGlobalTag    = "GR_E_V33A::All"
hltmonGlobalTag     = "GR_E_V29::All"
alcap0GlobalTag     = "GR_P_V43D::All"

# Splitting parameters for PromptReco
defaultRecoSplitting = 5000 
hiRecoSplitting = 1000
alcarawSplitting = 100000

#
# Setup repack and express mappings
#
repackVersionOverride = {
    "CMSSW_5_0_0" : "CMSSW_5_1_2_patch1",
    "CMSSW_5_0_1" : "CMSSW_5_1_2_patch1",
    "CMSSW_5_1_1" : "CMSSW_5_1_2_patch1",
    "CMSSW_5_1_2" : "CMSSW_5_1_2_patch1",
    "CMSSW_5_2_2" : "CMSSW_5_3_14",
    "CMSSW_5_2_3" : "CMSSW_5_3_14",
    "CMSSW_5_2_4" : "CMSSW_5_3_14",
    "CMSSW_5_2_5" : "CMSSW_5_3_14",
    "CMSSW_5_2_6" : "CMSSW_5_3_14",
    "CMSSW_5_2_7" : "CMSSW_5_3_14",
    "CMSSW_5_2_8" : "CMSSW_5_3_14",
    "CMSSW_5_2_9" : "CMSSW_5_3_14",
    }
expressVersionOverride = {
    "CMSSW_5_0_0" : "CMSSW_5_1_2_patch1",
    "CMSSW_5_0_1" : "CMSSW_5_1_2_patch1",
    "CMSSW_5_1_1" : "CMSSW_5_1_2_patch1",
    "CMSSW_5_1_2" : "CMSSW_5_1_2_patch1",
    "CMSSW_5_2_2" : "CMSSW_5_3_14",
    "CMSSW_5_2_3" : "CMSSW_5_3_14",
    "CMSSW_5_2_4" : "CMSSW_5_3_14",
    "CMSSW_5_2_5" : "CMSSW_5_3_14",
    "CMSSW_5_2_6" : "CMSSW_5_3_14",
    "CMSSW_5_2_7" : "CMSSW_5_3_14",
    "CMSSW_5_2_8" : "CMSSW_5_3_14",
    "CMSSW_5_2_9" : "CMSSW_5_3_14",
    }

hltmonVersionOverride = {
    "CMSSW_5_0_0" : "CMSSW_5_1_2_patch1",
    "CMSSW_5_0_1" : "CMSSW_5_1_2_patch1",
    "CMSSW_5_1_1" : "CMSSW_5_1_2_patch1",
    "CMSSW_5_1_2" : "CMSSW_5_1_2_patch1",
    "CMSSW_5_2_2" : "CMSSW_5_2_7_hltpatch1",
    "CMSSW_5_2_3" : "CMSSW_5_2_7_hltpatch1",
    "CMSSW_5_2_4" : "CMSSW_5_2_7_hltpatch1",
    "CMSSW_5_2_5" : "CMSSW_5_2_7_hltpatch1",
    "CMSSW_5_2_6" : "CMSSW_5_2_7_hltpatch1",
    "CMSSW_5_2_7" : "CMSSW_5_2_7_hltpatch1",
    "CMSSW_5_2_8" : "CMSSW_5_2_7_hltpatch1",
    "CMSSW_5_2_9" : "CMSSW_5_2_7_hltpatch1",
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
                maxInputEvents = 10 * 1000 * 1000,
                maxInputFiles = 1000,
                versionOverride = repackVersionOverride)

addDataset(tier0Config, "Default",
           do_reco = False,
           write_reco = False, write_aod = True, write_dqm = True,
           reco_delay = defaultRecoTimeout,
           reco_delay_offset = defaultRecoLockTimeout,
           reco_split = defaultRecoSplitting,
           proc_version = defaultProcVersion,
           cmssw_version = defaultCMSSWVersion,
           global_tag = promptrecoGlobalTag,
           archival_node = "T0_CH_CERN",
           scenario = "pp")


###############################
### PDs used during Run2012 ###
###############################

# special scouting PD for parked data
addDataset(tier0Config, "DataScouting",
           do_reco = True,
           write_reco = False, write_aod = False, write_dqm = True,
           reco_split = 3 * defaultRecoSplitting,
           dqm_sequences = [ "@common" ],
           scenario = "cosmics")

addDataset(tier0Config, "Cosmics",
           do_reco = True,
           alca_producers = [ "TkAlCosmics0T", "MuAlGlobalCosmics", "HcalCalHOCosmics", "DtCalibCosmics" ],
           scenario = "cosmics")
addDataset(tier0Config, "JetHT",
           do_reco = True,
           dqm_sequences = [ "@common", "@jetmet" ],
           scenario = "pp")
addDataset(tier0Config, "MET",
           do_reco = True,
           dqm_sequences = [ "@common", "@jetmet", "@hcal" ],
           scenario = "pp")
addDataset(tier0Config, "SingleMu",
           do_reco = True,
           alca_producers = [ "MuAlCalIsolatedMu", "MuAlOverlaps", "TkAlMuonIsolated", "DtCalib" ],
           dqm_sequences = [ "@common", "@muon", "@jetmet" ],
           scenario = "pp")
addDataset(tier0Config, "DoubleMu",
           do_reco = True,
           alca_producers = [ "MuAlCalIsolatedMu", "MuAlOverlaps", "DtCalib", "TkAlZMuMu" ],
           dqm_sequences = [ "@common", "@muon", "@egamma" ],
           scenario = "pp")
addDataset(tier0Config, "MuOnia",
           do_reco = True,
           alca_producers = [ "TkAlJpsiMuMu", "TkAlUpsilonMuMu" ],
           dqm_sequences = [ "@common" ],
           scenario = "pp")
addDataset(tier0Config, "SinglePhoton",
           do_reco = True,
           dqm_sequences = [ "@common", "@ecal", "@egamma" ],
           scenario = "pp")
addDataset(tier0Config, "DoublePhoton",
           do_reco = True,
           dqm_sequences = [ "@common", "@ecal", "@egamma" ],
           scenario = "pp")
addDataset(tier0Config, "DoublePhotonHighPt",
           do_reco = True,
           dqm_sequences = [ "@common", "@ecal", "@egamma" ],
           scenario = "pp")
addDataset(tier0Config, "SingleElectron",
           do_reco = True,
           alca_producers = [ "EcalCalElectron" ],
           dqm_sequences = [ "@common", "@ecal" ],
           scenario = "pp")
addDataset(tier0Config, "DoubleElectron",
           do_reco = True,
           alca_producers = [ "EcalCalElectron" ],
           dqm_sequences = [ "@common" ],
           scenario = "pp")
addDataset(tier0Config, "Commissioning",
           do_reco = True,
           alca_producers = [ "HcalCalIsoTrk" ],
           scenario = "pp")
addDataset(tier0Config, "ParkingMonitor",
           do_reco = True,
           dqm_sequences = [ "@common", "@muon", "@hcal", "@jetmet", "@ecal", "@egamma" ],
           scenario = "pp")

datasets = [ "BJetPlusX", "BTag", "MultiJet", "MuEG", "MuHad"," ElectronHad",
             "PhotonHad", "HTMHT", "Tau", "TauPlusX", "NoBPTX", "JetMon" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = "pp")

datasets = [ "MinimumBias", "MinimumBias1", "MinimumBias2" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               alca_producers = [ "TkAlMinBias", "SiStripCalMinBias" ],
               dqm_sequences = [ "@commonSiStripZeroBias", "@ecal", "@hcal", "@muon" ],
               scenario = "pp")

datasets = [ "L1Accept", "HcalHPDNoise", "LogMonitor", "RPCMonitor", "FEDMonitor" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False)


########################
### special test PDs ###
########################

addDataset(tier0Config, "HcalNZS",
           do_reco = True,
           alca_producers = [ "HcalCalMinBias" ],
           scenario = "hcalnzs")
addDataset(tier0Config,"TestEnablesEcalHcalDT",
           do_reco = False,
           scenario = "AlCaTestEnable")
addDataset(tier0Config,"TestEnablesTracker",
           do_reco = True,
           write_reco = False, write_aod = False, write_dqm = True,
           alca_producers = [ "TkAlLAS" ],
           scenario = "AlCaTestEnable")


###########################
### special AlcaRaw PDs ###
###########################

addDataset(tier0Config,"AlCaP0",
           do_reco = False,
           write_reco = False, write_aod = False, write_dqm = True,
           reco_split = alcarawSplitting,
           proc_version = alcarawProcVersion,
           global_tag = alcap0GlobalTag,
           scenario = "AlCaP0")
addDataset(tier0Config,"AlCaPhiSym",
           do_reco = False,
           write_reco = False, write_aod = False, write_dqm = True,
           reco_split = alcarawSplitting,
           proc_version = alcarawProcVersion,
           scenario = "AlCaPhiSymEcal")
addDataset(tier0Config,"AlCaLumiPixels",
           do_reco = True,
           write_reco = False, write_aod = False, write_dqm = True,
           reco_split = alcarawSplitting,
           proc_version = alcarawProcVersion,
           alca_producers = [ "LumiPixels" ],
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
               scenario = "pp")


############################
### HI proton-lead tests ###
############################

datasets = [ "PAPhysics", "PAZeroBias1", "PAZeroBias2", ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               reco_split = hiRecoSplitting,
               scenario = "pp")


###############################
### Heavy Ion 2013 datasets ###
###############################

addDataset(tier0Config, "PAMinBiasUPC",
           do_reco = True,
           reco_split = hiRecoSplitting,
           alca_producers = [ "SiStripCalMinBias", "TkAlMinBias" ],
           scenario = "pp")

addDataset(tier0Config, "PAMuon",
           do_reco = True,
           reco_split = hiRecoSplitting,
           alca_producers = [ "TkAlMuonIsolated", "DtCalib" ],
           scenario = "pp")

datasets = [ "PAHighPt", "PAMinBias1", "PAMinBias2" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               reco_split = hiRecoSplitting,
               scenario = "pp")


########################################################
### ZeroBias PDs - extra ones used for various tests ###
########################################################

datasets = [ "ZeroBias", "ZeroBias1", "ZeroBias2", "ZeroBias3", "ZeroBias4",
             "ZeroBias5", "ZeroBias6", "ZeroBias7", "ZeroBias8", "ZeroBiasVdm" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = "pp")

#################################
### PDs used for High PU runs ###
#################################

datasets = [ "HighPileUpHPF", "L1EGHPF", "L1MuHPF", "L1JetHPF",
             "ZeroBiasHPF0","HLTPhysics1", "HLTPhysics2" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = "pp")


#####################
### 25ns datasets ###
#####################

addDataset(tier0Config, "Cosmics25ns",
           do_reco = True,
           alca_producers = ["TkAlCosmics0T", "MuAlGlobalCosmics", "HcalCalHOCosmics", "DtCalibCosmics"],
           scenario = "cosmics")
addDataset(tier0Config, "DoubleElectron25ns",
           do_reco = True,
           alca_producers = ["EcalCalElectron"],
           scenario = "pp")
addDataset(tier0Config, "DoubleMu25ns",
           do_reco = True,
           alca_producers = ["MuAlCalIsolatedMu", "MuAlOverlaps", "DtCalib", "TkAlZMuMu"],
           scenario = "pp")
addDataset(tier0Config, "DoubleMuParked25ns",
           do_reco = True,
           alca_producers = ["MuAlCalIsolatedMu", "MuAlOverlaps", "DtCalib", "TkAlZMuMu"],
           scenario = "pp")
addDataset(tier0Config,"HcalNZS25ns",
           do_reco = True,
           alca_producers = ["HcalCalMinBias"],
           scenario = "hcalnzs")
addDataset(tier0Config,"MinimumBias25ns",
           do_reco = True,
           alca_producers = ["SiStripCalMinBias", "TkAlMinBias"],
           scenario = "pp")
addDataset(tier0Config,"SingleMu25ns",
           do_reco = True,
           alca_producers = ["MuAlCalIsolatedMu", "MuAlOverlaps", "TkAlMuonIsolated", "DtCalib"],
           scenario = "pp")

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
               scenario = "pp")

datasets = [ "HcalHPDNoise25ns", "LogMonitor25ns", "FEDMonitor25ns" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = False)


#############################
### Express configuration ###
#############################

addExpressConfig(tier0Config, "HIExpress",
                 scenario = "HeavyIons",
                 data_tiers = [ "FEVT", "ALCARECO", "DQM" ],
                 alca_producers = [ "SiStripCalZeroBias", "TkAlMinBiasHI", "PromptCalibProd" ],
                 global_tag = expressGlobalTag,
                 proc_ver = expressProcVersion,
                 maxInputEvents = 200,
                 maxInputSize = 2 * 1024 * 1024 * 1024,
                 maxInputFiles = 500,
                 maxLatency = 5 * 23,
                 blockCloseDelay = 3600,
                 versionOverride = expressVersionOverride)

addExpressConfig(tier0Config, "Express",
                 scenario = "pp",
                 data_tiers = [ "FEVT", "ALCARECO", "DQM" ],
                 alca_producers = [ "SiStripCalZeroBias", "TkAlMinBias", "MuAlCalIsolatedMu", "DtCalib", "PromptCalibProd" ],
                 dqm_sequences = [ "@common", "@jetmet" ],
#                 reco_version = defaultRecoVersion,
                 global_tag = expressGlobalTag,
                 proc_ver = expressProcVersion,
                 maxInputEvents = 200,
                 maxInputSize = 2 * 1024 * 1024 * 1024,
                 maxInputFiles = 500,
                 maxLatency = 15 * 23,
                 blockCloseDelay = 3600,
                 versionOverride = expressVersionOverride)

addExpressConfig(tier0Config, "ExpressCosmics",
                 scenario = "cosmics",
                 data_tiers = [ "FEVT", "ALCARECO", "DQM" ],
                 alca_producers = [ "SiStripCalZeroBias", "TkAlCosmics0T" ],
                 global_tag = expressGlobalTag,
                 proc_ver = expressProcVersion,
                 maxInputEvents = 200,
                 maxInputSize = 2 * 1024 * 1024 * 1024,
                 maxInputFiles = 500,
                 maxLatency = 15 * 23,
                 blockCloseDelay = 3600,
                 versionOverride = expressVersionOverride)

addExpressConfig(tier0Config, "HLTMON",
                 scenario = "pp",
                 data_tiers = [ "FEVTHLTALL", "DQM" ],
                 global_tag = hltmonGlobalTag,
                 proc_ver = expressProcVersion,
                 maxInputEvents = 200,
                 maxInputSize = 2 * 1024 * 1024 * 1024,
                 maxInputFiles = 500,
                 maxLatency = 15 * 23,
                 blockCloseDelay = 3600,
                 versionOverride = hltmonVersionOverride)


###################################
### currently inactive settings ###
###################################

##ignoreStream(tier0Config, "Express")
##
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
