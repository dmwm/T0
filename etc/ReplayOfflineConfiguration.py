"""
_OfflineConfiguration_
Processing configuration for the Tier0 - Replay version
"""
from __future__ import print_function

import datetime
import json
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
from T0.RunConfig.Tier0Config import loadConfig
from T0.RunConfig.Tier0Config import addRepackConfig
from T0.RunConfig.Tier0Config import addExpressConfig
from T0.RunConfig.Tier0Config import setInjectRuns
from T0.RunConfig.Tier0Config import setStreamerPNN
from T0.RunConfig.Tier0Config import setEnableUniqueWorkflowName

# Create the Tier0 configuration object
tier0Config = createTier0Config()

# Load replay configuration dictionary
replayConfig = loadConfig("/data/tier0/admin/configurations/ReplayConfiguration.json")
# Set run number to replay
setInjectRuns(tier0Config, replayConfig["runs"])

# Set global parameters:
setAcquisitionEra(tier0Config, replayConfig["acquisitionEra"])
setBaseRequestPriority(tier0Config, replayConfig["acquisitionEra"])
setBackfill(tier0Config, replayConfig["backfill"])
setBulkDataType(tier0Config, replayConfig["bulkDataType"])
setProcessingSite(tier0Config, replayConfig["processingSite"])
setStreamerPNN(tier0Config, replayConfig["streamerPNN"])

# Override for DQM data tier and server
dqmConfig = loadConfig("/data/tier0/admin/configurations/DQM.json")
setDQMDataTier(tier0Config, dqmConfig["DQMIODataTier"])
setDQMUploadUrl(tier0Config, dqmConfig["DQMUploadUrl"])

# Set unique replay workflow names
# Uses era name, Repack, Express, PromptReco processing versions, date/time, e.g.:
# PromptReco_Run322057_Charmonium_Tier0_REPLAY_vocms047_v274_190221_121
setEnableUniqueWorkflowName(tier0Config)

# Define the two default timeouts for reco release
# First timeout is used directly for reco release
# Second timeout is used for the data service PromptReco start check
# (to basically say we started PromptReco even though we haven't)

promptRecoConfig = loadConfig("/data/tier0/admin/configurations/PromptReco.json")

# PCL parameters
setPromptCalibrationConfig(tier0Config, **promptRecoConfig)


# Special syntax supported for cmssw version, processing version and global tag
#
# { 'acqEra': {'Era1': Value1, 'Era2': Value2},
#   'maxRun': {100000: Value3, 200000: Value4},
#   'default': Value5 }

# Configure ScramArch
setDefaultScramArch(tier0Config, replayConfig["scramArch"])

# Configure scenarios
scenarios = loadConfig("/data/tier0/admin/configurations/Scenarios.json")

# Procesing version number replays
dt = int(datetime.datetime.now().strftime("%y%m%d%H%M"))
defaultProcVersion = dt
expressProcVersion = dt
alcarawProcVersion = dt


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
    "CMSSW_11_2_4" : defaultCMSSWVersion['default']
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
    "CMSSW_11_2_4" : defaultCMSSWVersion['default']
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
                versionOverride=repackVersionOverride)

options=loadConfig("/data/tier0/admin/configurations/Datasets/Default.json")
addDataset(tier0Config, "Default",
           reco_delay=defaultRecoTimeout,
           reco_delay_offset=defaultRecoLockTimeout,
           reco_split=defaultRecoSplitting,
           proc_version=defaultProcVersion,
           cmssw_version=defaultCMSSWVersion,
           multicore=numberOfCores,
           global_tag=promptrecoGlobalTag,
           global_tag_connect=globalTagConnect,
           scenario=ppScenario,
           **options)

#############################
### Express configuration ###
#############################
options=loadConfig("/data/tier0/admin/configurations/Express/Express.json")
addExpressConfig(tier0Config, "Express",
                 scenario=ppScenario,
                 reco_version=defaultCMSSWVersion,
                 multicore=numberOfCores,
                 global_tag_connect=globalTagConnect,
                 global_tag=expressGlobalTag,
                 proc_ver=expressProcVersion,
                 versionOverride=expressVersionOverride,
                 **options
                 )

options=loadConfig("/data/tier0/admin/configurations/Express/ExpressCosmics.json")
addExpressConfig(tier0Config, "ExpressCosmics",
                 scenario=cosmicsScenario,
                 reco_version=defaultCMSSWVersion,
                 multicore=numberOfCores,
                 global_tag_connect=globalTagConnect,
                 global_tag=expressGlobalTag,
                 proc_ver=expressProcVersion,
                 versionOverride=expressVersionOverride,
                 **options)


###################################
### Standard Physics PDs (2017) ###
###################################


DATASETS = ["Cosmics"]
options=loadConfig("/data/tier0/admin/configurations/Datasets/Cosmics.json")
for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               scenario=cosmicsScenario,
               **options)


#############################################
### Standard Commisioning PDs (2017)      ###
#############################################

options=loadConfig("/data/tier0/admin/configurations/Datasets/Commissioning.json")
DATASETS = ["Commissioning"]
DATASETS += ["Commissioning1", "Commissioning2", "Commissioning3", "Commissioning4",
             "CommissioningMuons", "CommissioningEGamma", "CommissioningTaus", "CommissioningSingleJet", "CommissioningDoubleJet"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               scenario=ppScenario,
               **options)

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
