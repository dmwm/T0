"""
_ExampleConfig_

Example configuration for RunConfig unittest

"""
from T0.RunConfig.Tier0Config import addDataset
from T0.RunConfig.Tier0Config import createTier0Config
from T0.RunConfig.Tier0Config import setAcquisitionEra
from T0.RunConfig.Tier0Config import setRecoTimeout
from T0.RunConfig.Tier0Config import setRecoLockTimeout
from T0.RunConfig.Tier0Config import setConfigVersion
from T0.RunConfig.Tier0Config import ignoreStream
from T0.RunConfig.Tier0Config import addRepackConfig
from T0.RunConfig.Tier0Config import addExpressConfig
from T0.RunConfig.Tier0Config import addRegistrationConfig
from T0.RunConfig.Tier0Config import addConversionConfig
from T0.RunConfig.Tier0Config import addTier1Skim

# Create the Tier0 configuration object
tier0Config = createTier0Config()

# Set global parameters like the acquisition era
# and the version of the configuration.
setAcquisitionEra(tier0Config, "ExampleConfig_UnitTest")
setConfigVersion(tier0Config, "replace with real version")

# Set the two timeouts for reco release
# First timeout is used directly for reco release
# Second timeout is used for the data service PromptReco start check
# (to basically say we started PromptReco even though we haven't)
setRecoTimeout(tier0Config, 60)
setRecoLockTimeout(tier0Config, 30)

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
                versionOverride = repackVersionOverride)

addExpressConfig(tier0Config, "Express",
                 scenario = "pp",
                 data_tiers = [ "FEVT", "ALCARECO", "DQM" ],
                 alca_producers = [ "SiStripCalZeroBias", "PromptCalibProd" ],
                 global_tag = "GlobalTag1",
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
           reco_version = "CMSSW_4_2_8_patch1",
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
