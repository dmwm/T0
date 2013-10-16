"""
_ExampleConfig_

Example configuration for RunConfig unittest

"""
from T0.RunConfig.Tier0Config import addDataset
from T0.RunConfig.Tier0Config import createTier0Config
from T0.RunConfig.Tier0Config import setAcquisitionEra
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
from T0.RunConfig.Tier0Config import addTier1Skim

# Create the Tier0 configuration object
tier0Config = createTier0Config()

# set the config version (not really used at the moment)
setConfigVersion(tier0Config, "replace with real version")

# Set global parameters:
#  acquisition era
#  LFN prefix
#  data type
setAcquisitionEra(tier0Config, "ExampleConfig_UnitTest")
setLFNPrefix(tier0Config, "/store")
setBulkDataType(tier0Config, "data")
setBulkDataLocation(tier0Config, "T2_CH_CERN")
setDQMUploadUrl(tier0Config, "https://cmsweb.cern.ch/dqm/dev")
setPromptCalibrationConfig(tier0Config,
                           alcaHarvestTimeout = 12*3600,
                           alcaHarvestDir = "/some/afs/dir",
                           conditionUploadTimeout = 18*3600,
                           dropboxHost = "webcondvm.cern.ch",
                           validationMode = True)

# setup repack and express version mappings
repackVersionOverride = {
    }
expressVersionOverride = {
    "CMSSW_4_2_7" : "CMSSW_4_2_8_patch6",
    }
hltmonVersionOverride = {
    "CMSSW_4_2_7" : "CMSSW_4_2_8_patch7",
    }

addRepackConfig(tier0Config, "Default",
                proc_ver = 1,
                maxSizeSingleLumi = 1234,
                maxSizeMultiLumi = 1122,
                minInputSize = 210,
                maxInputSize = 400,
                maxEdmSize = 1233,
                maxOverSize = 1133,
                maxInputEvents = 500,
                maxInputFiles = 1111,
                versionOverride = repackVersionOverride)

addExpressConfig(tier0Config, "Express",
                 scenario = "pp",
                 data_tiers = [ "FEVT", "ALCARECO", "DQM" ],
                 maxInputEvents = 123,
                 maxInputSize = 123456789,
                 maxInputFiles = 1234,
                 maxLatency = 12 * 23,
                 alca_producers = [ "SiStripCalZeroBias", "PromptCalibProd" ],
                 dqm_sequences = [ "@common" ],
                 global_tag = "GlobalTag1",
                 reco_version = "CMSSW_4_2_8_patch7",
                 proc_ver = 2,
                 versionOverride = expressVersionOverride)

addExpressConfig(tier0Config, "HLTMON",
                 scenario = "cosmics",
                 data_tiers = [ "FEVTHLTALL" ],
                 global_tag = "GlobalTag2",
                 proc_ver = 3,
                 versionOverride = hltmonVersionOverride)

addDataset(tier0Config, "Default",
           scenario = "pp",
           reco_delay = 60, reco_delay_offset = 30,
           reco_version = "CMSSW_4_2_8_patch1",
           scram_arch = "slc5_amd64_gcc462",
           default_proc_ver = 4,
           global_tag = "GlobalTag3",
           archival_node = "Node1")

addDataset(tier0Config, "Cosmics",
           scenario = "cosmics",
           do_reco = True,
           global_tag = "GlobalTag4",
           reco_split = 100,
           alca_producers = [ "Skim1", "Skim2", "Skim3" ],
           reco_version = "CMSSW_4_2_8_patch2",
           reco_proc_ver = 5,
           do_alca = True,
           custodial_node = "Node2",
           archival_node = "Node3",
           write_reco = True,
           write_aod = True,
           write_dqm = True)

addDataset(tier0Config, "MinimumBias",
           scenario = "pp",
           do_reco = False,
           global_tag = "GlobalTag5",
           reco_split = 200,
           alca_producers = [],
           reco_version = "CMSSW_4_2_8_patch3",
           reco_proc_ver = 6,
           do_alca = False,
           custodial_node = "Node4",
           archival_node = "Node5",
           custodial_priority = "normal",
           custodial_auto_approve = True,
           write_reco = False,
           write_aod = False,
           write_dqm = False)

addTier1Skim(tier0Config,"Skim1",
             dataTier = "RECO",
             primaryDataset = "Cosmics",
             cmsswVersion = "CMSSW_4_2_8_patch4",
             processingVersion = 7,
             configURL = "exampleurl1",
             globalTag = "GlobalTag6",
             twoFileRead = True)

addTier1Skim(tier0Config,"Skim2",
             dataTier = "AOD",
             primaryDataset = "MinimumBias",
             cmsswVersion = "CMSSW_4_2_8_patch5",
             processingVersion = 8,
             configURL = "exampleurl2",
             globalTag = "GlobalTag7",
             twoFileRead = False,
             skimNode = "Node6")

if __name__ == '__main__':
    print tier0Config
