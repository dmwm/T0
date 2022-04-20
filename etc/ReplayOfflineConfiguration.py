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

# Create the Tier0 configuration object
tier0Config = createTier0Config()

# Set the verstion configuration (not used at the moment)
setConfigVersion(tier0Config, "replace with real version")

# Set run number to replay
setInjectRuns(tier0Config, [346512])

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
    'default': "CMSSW_12_4_0_pre3"
}

# Configure ScramArch
setDefaultScramArch(tier0Config, "slc7_amd64_gcc10")

# Configure scenarios
ppScenario = "ppEra_Run3"
ppScenarioB0T = "ppEra_Run3"
cosmicsScenario = "cosmicsEra_Run3"
hcalnzsScenario = "hcalnzsEra_Run3"
hiScenario = "ppEra_Run3"
alcaTrackingOnlyScenario = "trackingOnlyEra_Run3"
alcaTestEnableScenario = "AlCaTestEnable"
alcaLumiPixelsScenario = "AlCaLumiPixels"
alcaPhiSymEcalScenario = "AlCaPhiSymEcal_Nano"
hiTestppScenario = "ppEra_Run3"


# Procesing version number replays
dt = 212
defaultProcVersion = dt
expressProcVersion = dt
alcarawProcVersion = dt

# Defaults for GlobalTag
expressGlobalTag = "123X_dataRun3_Express_v5"
promptrecoGlobalTag = "123X_dataRun3_Prompt_v6"
alcap0GlobalTag = "123X_dataRun3_Prompt_v6"

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
    "CMSSW_12_0_2_patch2" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_3" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_3_patch1" : defaultCMSSWVersion['default'],
    "CMSSW_12_2_1" : defaultCMSSWVersion['default'],
    "CMSSW_12_2_1_patch1" : defaultCMSSWVersion['default'],
    "CMSSW_12_2_2" : defaultCMSSWVersion['default'],
    "CMSSW_12_2_3" : defaultCMSSWVersion['default']
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
    "CMSSW_12_0_2_patch1" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_2_patch2" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_3" : defaultCMSSWVersion['default'],
    "CMSSW_12_0_3_patch1" : defaultCMSSWVersion['default'],
    "CMSSW_12_2_1" : defaultCMSSWVersion['default'],
    "CMSSW_12_2_1_patch1" : defaultCMSSWVersion['default'],
    "CMSSW_12_2_2" : defaultCMSSWVersion['default'],
    "CMSSW_12_2_3" : defaultCMSSWVersion['default']
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
           maxMemoryperCore=2000,
           scenario=ppScenario)


DATASETS = ["AlCaPhiSym"]

for dataset in DATASETS:
    addDataset(tier0Config, dataset,
               do_reco=False,
               raw_to_disk=True,
               disk_node="T2_CH_CERN"
               alca_producers=["EcalPhiSymByRun"],
               scenario=alcaPhiSymEcalScenario)

#######################
### ignored streams ###
#######################

ignoreStream(tier0Config, "ALCALumiPixelsCountsExpress")
ignoreStream(tier0Config, "ALCALumiPixelsCountsPrompt")
ignoreStream(tier0Config, "Calibration")
ignoreStream(tier0Config, "Express")
ignoreStream(tier0Config, "ExpressAlignment")
ignoreStream(tier0Config, "HLTMonitor")
ignoreStream(tier0Config, "NanoDST")
ignoreStream(tier0Config, "Physics")
ignoreStream(tier0Config, "PhysicsMinimumBias0")
ignoreStream(tier0Config, "PhysicsMinimumBias1")
ignoreStream(tier0Config, "PhysicsMinimumBias2")
ignoreStream(tier0Config, "PhysicsMinimumBias3")
ignoreStream(tier0Config, "PhysicsMinimumBias4")
ignoreStream(tier0Config, "PhysicsMinimumBias5")
ignoreStream(tier0Config, "PhysicsMinimumBias6")
ignoreStream(tier0Config, "PhysicsMinimumBias7")
ignoreStream(tier0Config, "PhysicsMinimumBias8")
ignoreStream(tier0Config, "PhysicsMinimumBias9")
ignoreStream(tier0Config, "PhysicsZeroBias0")
ignoreStream(tier0Config, "PhysicsZeroBias10")
ignoreStream(tier0Config, "PhysicsZeroBias1")
ignoreStream(tier0Config, "PhysicsZeroBias11")
ignoreStream(tier0Config, "PhysicsZeroBias12")
ignoreStream(tier0Config, "PhysicsZeroBias13")
ignoreStream(tier0Config, "PhysicsZeroBias14")
ignoreStream(tier0Config, "PhysicsZeroBias15")
ignoreStream(tier0Config, "PhysicsZeroBias16")
ignoreStream(tier0Config, "PhysicsZeroBias17")
ignoreStream(tier0Config, "PhysicsZeroBias18")
ignoreStream(tier0Config, "PhysicsZeroBias19")
ignoreStream(tier0Config, "PhysicsZeroBias2")
ignoreStream(tier0Config, "PhysicsZeroBias3")
ignoreStream(tier0Config, "PhysicsZeroBias4")
ignoreStream(tier0Config, "PhysicsZeroBias5")
ignoreStream(tier0Config, "PhysicsZeroBias6")
ignoreStream(tier0Config, "PhysicsZeroBias7")
ignoreStream(tier0Config, "PhysicsZeroBias8")
ignoreStream(tier0Config, "PhysicsZeroBias9")

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
