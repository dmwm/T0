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
setAcquisitionEra(tier0Config, "Run2015A")
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
defaultCMSSWVersion = "CMSSW_7_4_4_patch1"

# Configure ScramArch
setDefaultScramArch(tier0Config, "slc6_amd64_gcc491")

# Configure scenarios
cosmicsScenario = "cosmicsRun2"
ppScenario = "ppRun2B0T"
hcalnzsScenario = "hcalnzsRun2"

# Defaults for processing version
defaultProcVersionRAW = 1
defaultProcVersionReco = 1
expressProcVersion = 1
alcarawProcVersion = 1

# Defaults for GlobalTag
expressGlobalTag = "GR_E_V48"
promptrecoGlobalTag = "GR_P_V55"
alcap0GlobalTag = "GR_P_V55"

globalTagConnect = "frontier://PromptProd/CMS_CONDITIONS"

# Splitting parameters for PromptReco
defaultRecoSplitting = 2000
hiRecoSplitting = 1000
alcarawSplitting = 100000

#
# Setup repack and express mappings
#
repackVersionOverride = {
    "CMSSW_7_4_2" : "CMSSW_7_4_4_patch1",
    "CMSSW_7_4_3" : "CMSSW_7_4_4_patch1",
    "CMSSW_7_4_4" : "CMSSW_7_4_4_patch1",
    }
expressVersionOverride = {
    "CMSSW_7_4_2" : "CMSSW_7_4_4_patch1",
    "CMSSW_7_4_3" : "CMSSW_7_4_4_patch1",
    "CMSSW_7_4_4" : "CMSSW_7_4_4_patch1",
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
           scenario = ppScenario)


###############################
### PDs used during Run2015 ###
###############################

addDataset(tier0Config, "Cosmics",
           do_reco = True,
           alca_producers = [ "TkAlCosmics0T", "MuAlGlobalCosmics", "HcalCalHOCosmics", "DtCalibCosmics" ],
           scenario = cosmicsScenario)
addDataset(tier0Config, "SingleMu",
           do_reco = True,
           dqm_sequences = [ "@common", "@muon", "@jetmet" ],
           scenario = ppScenario)
addDataset(tier0Config, "Commissioning",
           do_reco = True,
	   alca_producers = [ "TkAlMinBias", "SiStripCalZeroBias", "SiStripCalMinBias" ],
           scenario = ppScenario)

datasets = [ "NoBPTX" ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               dqm_sequences = [ "@common" ],
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
               alca_producers = [ "TkAlMinBias", "SiStripCalZeroBias", "SiStripCalMinBias" ],
               dqm_sequences = [ "@commonSiStripZeroBias", "@ecal", "@hcal", "@muon" ],
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
           write_reco = False, write_aod = False, write_dqm = True,
           reco_split = alcarawSplitting,
           proc_version = alcarawProcVersion,
           alca_producers = [ "LumiPixels" ],
           scenario = "AlCaLumiPixels")

########################################################
### ZeroBias PDs                                     ###
########################################################

datasets = [ "ZeroBias1", "ZeroBias2", "ZeroBias3", "ZeroBias4",
             "ZeroBias5", "ZeroBias6", "ZeroBias7", "ZeroBias8"  ]

for dataset in datasets:
    addDataset(tier0Config, dataset,
               do_reco = True,
               scenario = ppScenario)

#############################
### Express configuration ###
#############################

addExpressConfig(tier0Config, "Express",
                 scenario = ppScenario,
                 data_tiers = [ "FEVT" ],
                 write_dqm = True,
                 alca_producers = [ "SiStripPCLHistos", "SiStripCalZeroBias", "TkAlMinBias", "PromptCalibProd", "PromptCalibProdSiStrip" ],
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
                 scenario = cosmicsScenario,
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
