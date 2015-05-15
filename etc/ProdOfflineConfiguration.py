"""
_OfflineConfiguration_

Processing configuration for the Tier0 - Production version
"""

from T0.RunConfig.Tier0Config import addDataset
from T0.RunConfig.Tier0Config import createTier0Config
from T0.RunConfig.Tier0Config import setAcquisitionEra
from T0.RunConfig.Tier0Config import setScramArch
from T0.RunConfig.Tier0Config import setDefaultScramArch
from T0.RunConfig.Tier0Config import setBackfill
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
from T0.RunConfig.Tier0Config import setDQMDataTier

# Create the Tier0 configuration object
tier0Config = createTier0Config()

# Set the verstion configuration (not used at the moment)
setConfigVersion(tier0Config, "replace with real version")

# Set global parameters:
#  Acquisition era
#  LFN prefix
#  Data type
#  PhEDEx location for Bulk data
setAcquisitionEra(tier0Config, "Commissioning2015")
setBackfill(tier0Config, None)
setBulkDataType(tier0Config, "data")
setBulkDataLocation(tier0Config, "T2_CH_CERN")

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
defaultCMSSWVersion = "CMSSW_7_4_2"

# Configure ScramArch
setDefaultScramArch(tier0Config, "slc6_amd64_gcc491")

# Defaults for processing version
defaultProcVersionRAW = 1
defaultProcVersionReco = 1
expressProcVersion = 1
alcarawProcVersion = 1

# Defaults for GlobalTag
expressGlobalTag = "GR_E_V47"
promptrecoGlobalTag = "GR_P_V54"
alcap0GlobalTag = "GR_P_V54"

globalTagConnect = "frontier://PromptProd/CMS_CONDITIONS"

# Splitting parameters for PromptReco
defaultRecoSplitting = 2000
hiRecoSplitting = 1000
alcarawSplitting = 100000

#
# Setup repack and express mappings
#
repackVersionOverride = {
    }
expressVersionOverride = {
    }

#hltmonVersionOverride = {
#    "CMSSW_5_2_7" : "CMSSW_5_2_7_hltpatch1",
#    }

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
           write_reco = True, write_aod = True, write_dqm = True,
           reco_delay = defaultRecoTimeout,
           reco_delay_offset = defaultRecoLockTimeout,
           reco_split = defaultRecoSplitting,
           proc_version = defaultProcVersionReco,
           cmssw_version = defaultCMSSWVersion,
           global_tag = promptrecoGlobalTag,
           global_tag_connect = globalTagConnect,
           archival_node = "T0_CH_CERN_MSS",
           tape_node = "T1_US_FNAL_MSS",
           disk_node = "T1_US_FNAL_Disk",
	   blockCloseDelay = 24 * 3600,
           scenario = "ppRun2")


###############################
### PDs used during Run2012 ###
###############################

# special scouting PD for parked data
addDataset(tier0Config, "DataScouting",
           do_reco = True,
           write_reco = False, write_aod = False, write_dqm = True,
           reco_split = 3 * defaultRecoSplitting,
           dqm_sequences = [ "@common" ],
           scenario = "DataScouting")

addDataset(tier0Config, "Cosmics",
           do_reco = True,
           alca_producers = [ "TkAlCosmics0T", "MuAlGlobalCosmics", "HcalCalHOCosmics", "DtCalibCosmics" ],
           scenario = "cosmicsRun2")
addDataset(tier0Config, "JetHT",
           do_reco = True,
           dqm_sequences = [ "@common", "@jetmet" ],
           scenario = "ppRun2")
addDataset(tier0Config, "MET",
           do_reco = True,
           dqm_sequences = [ "@common", "@jetmet", "@hcal" ],
           scenario = "ppRun2")
addDataset(tier0Config, "SingleMu",
           do_reco = True,
#           alca_producers = [ "MuAlCalIsolatedMu", "MuAlOverlaps", "TkAlMuonIsolated", "DtCalib" ],
           dqm_sequences = [ "@common", "@muon", "@jetmet" ],
           scenario = "ppRun2")
addDataset(tier0Config, "DoubleMu",
           do_reco = True,
#           alca_producers = [ "MuAlCalIsolatedMu", "MuAlOverlaps", "DtCalib", "TkAlZMuMu" ],
           dqm_sequences = [ "@common", "@muon", "@egamma" ],
           scenario = "ppRun2")
addDataset(tier0Config, "MuOnia",
           do_reco = True,
#           alca_producers = [ "TkAlJpsiMuMu", "TkAlUpsilonMuMu" ],
           dqm_sequences = [ "@common" ],
           scenario = "ppRun2")
addDataset(tier0Config, "SinglePhoton",
           do_reco = True,
           dqm_sequences = [ "@common", "@ecal", "@egamma" ],
           scenario = "ppRun2")
addDataset(tier0Config, "DoublePhoton",
           do_reco = True,
           dqm_sequences = [ "@common", "@ecal", "@egamma" ],
           scenario = "ppRun2")
addDataset(tier0Config, "DoublePhotonHighPt",
           do_reco = True,
           dqm_sequences = [ "@common", "@ecal", "@egamma" ],
           scenario = "ppRun2")
addDataset(tier0Config, "SingleElectron",
           do_reco = True,
#           alca_producers = [ "EcalCalElectron" ],
           dqm_sequences = [ "@common", "@ecal" ],
           scenario = "ppRun2")
addDataset(tier0Config, "DoubleElectron",
           do_reco = True,
#           alca_producers = [ "EcalCalElectron" ],
           dqm_sequences = [ "@common" ],
           scenario = "ppRun2")
addDataset(tier0Config, "Commissioning",
           do_reco = True,
#           alca_producers = [ "HcalCalIsoTrk" ],
           scenario = "ppRun2")
addDataset(tier0Config, "ParkingMonitor",
           do_reco = True,
           dqm_sequences = [ "@common", "@muon", "@hcal", "@jetmet", "@ecal", "@egamma" ],
           scenario = "ppRun2")

datasets = [ "BJetPlusX", "BTag", "MultiJet", "MuEG", "MuHad"," ElectronHad",
             "PhotonHad", "HTMHT", "Tau", "TauPlusX", "NoBPTX", "JetMon" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
               scenario = "ppRun2")

datasets = [ "Jet", "Photon", "HT", "ForwardTriggers", "Interfill", "AllPhysics2760" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = "ppRun2")

datasets = [ "MinimumBias", "MinimumBias0", "MinimumBias1", "MinimumBias2",
             "MinBias0Tesla", "MinBias0Tesla0", "MinBias0Tesla1", "MinBias0Tesla2" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               alca_producers = [ "TkAlMinBias", "SiStripCalZeroBias", "SiStripCalMinBias" ],
               dqm_sequences = [ "@commonSiStripZeroBias", "@ecal", "@hcal", "@muon" ],
               scenario = "ppRun2")

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
           scenario = "hcalnzsRun2")
addDataset(tier0Config,"TestEnablesTracker",
           do_reco = True,
           write_reco = False, write_aod = False, write_dqm = True,
           alca_producers = [ "TkAlLAS" ],
           scenario = "AlCaTestEnable")
addDataset(tier0Config,"TestEnablesEcalHcalDT",
           do_reco = False,
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
#           alca_producers = [ "LumiPixels" ],
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
               scenario = "ppRun2")


############################
### HI proton-lead tests ###
############################

datasets = [ "PAPhysics", "PAZeroBias1", "PAZeroBias2", ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               reco_split = hiRecoSplitting,
               scenario = "ppRun2")


###############################
### Heavy Ion 2013 datasets ###
###############################

addDataset(tier0Config, "PAMinBiasUPC",
           do_reco = True,
           reco_split = hiRecoSplitting,
#           alca_producers = [ "SiStripCalMinBias", "TkAlMinBias" ],
           scenario = "ppRun2")

addDataset(tier0Config, "PAMuon",
           do_reco = True,
           reco_split = hiRecoSplitting,
#           alca_producers = [ "TkAlMuonIsolated", "DtCalib" ],
           scenario = "ppRun2")

datasets = [ "PAHighPt", "PAMinBias1", "PAMinBias2" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               reco_split = hiRecoSplitting,
               scenario = "ppRun2")


########################################################
### ZeroBias PDs - extra ones used for various tests ###
########################################################

datasets = [ "ZeroBias", "ZeroBias1", "ZeroBias2", "ZeroBias3", "ZeroBias4",
             "ZeroBias5", "ZeroBias6", "ZeroBias7", "ZeroBias8", "ZeroBiasVdm" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = "ppRun2")

#################################
### PDs used for High PU runs ###
#################################

datasets = [ "HighPileUpHPF", "L1EGHPF", "L1MuHPF", "L1JetHPF",
             "ZeroBiasHPF0","HLTPhysics1", "HLTPhysics2" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = "ppRun2")


#####################
### 25ns datasets ###
#####################

addDataset(tier0Config, "Cosmics25ns",
           do_reco = True,
#           alca_producers = ["TkAlCosmics0T", "MuAlGlobalCosmics", "HcalCalHOCosmics", "DtCalibCosmics"],
           scenario = "cosmicsRun2")
addDataset(tier0Config, "DoubleElectron25ns",
           do_reco = True,
#           alca_producers = ["EcalCalElectron"],
           scenario = "ppRun2")
addDataset(tier0Config, "DoubleMu25ns",
           do_reco = True,
#           alca_producers = ["MuAlCalIsolatedMu", "MuAlOverlaps", "DtCalib", "TkAlZMuMu"],
           scenario = "ppRun2")
addDataset(tier0Config, "DoubleMuParked25ns",
           do_reco = True,
#           alca_producers = ["MuAlCalIsolatedMu", "MuAlOverlaps", "DtCalib", "TkAlZMuMu"],
           scenario = "ppRun2")
addDataset(tier0Config,"HcalNZS25ns",
           do_reco = True,
#           alca_producers = ["HcalCalMinBias"],
           scenario = "hcalnzsRun2")
addDataset(tier0Config,"MinimumBias25ns",
           do_reco = True,
#           alca_producers = ["SiStripCalMinBias", "TkAlMinBias"],
           scenario = "ppRun2")
addDataset(tier0Config,"SingleMu25ns",
           do_reco = True,
#           alca_producers = ["MuAlCalIsolatedMu", "MuAlOverlaps", "TkAlMuonIsolated", "DtCalib"],
           scenario = "ppRun2")

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
               scenario = "ppRun2")

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
#		 alca_producers = [ "SiStripCalZeroBias", "TkAlMinBiasHI", "PromptCalibProd" ],
                 reco_version = defaultCMSSWVersion,
                 global_tag = expressGlobalTag,
		 global_tag_connect = globalTagConnect,
                 proc_ver = expressProcVersion,
                 maxInputRate = 23 * 1000,
                 maxInputEvents = 400,
                 maxInputSize = 2 * 1024 * 1024 * 1024,
                 maxInputFiles = 15,
                 maxLatency = 15 * 23,
                 periodicHarvestInterval = 20 * 60,
                 blockCloseDelay = 1200,
                 versionOverride = expressVersionOverride)

addExpressConfig(tier0Config, "Express",
                 scenario = "ppRun2",
                 data_tiers = [ "FEVT" ],
                 write_dqm = True,
                 alca_producers = [ "SiStripPCLHistos", "SiStripCalZeroBias", "TkAlMinBias", "PromptCalibProd" ],
                 reco_version = defaultCMSSWVersion,
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
                 scenario = "cosmicsRun2",
                 data_tiers = [ "FEVT" ],
                 write_dqm = True,
                 alca_producers = [ "SiStripPCLHistos", "SiStripCalZeroBias", "TkAlCosmics0T", "PromptCalibProdSiStrip" ],
                 reco_version = defaultCMSSWVersion,
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

#addExpressConfig(tier0Config, "HLTMON",
#                 scenario = "ppRun2",
#                 data_tiers = [ "FEVTHLTALL", "DQM" ],
#                 global_tag = hltmonGlobalTag,
#                 proc_ver = expressProcVersion,
#                 blockCloseDelay = 1200,
#                 versionOverride = hltmonVersionOverride)


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
