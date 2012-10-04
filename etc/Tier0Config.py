
config.component_('Tier0Feeder')
config.Tier0Feeder.namespace = "T0Component.Tier0Feeder.Tier0Feeder"
config.Tier0Feeder.componentDir = config.General.workDir + "/Tier0Feeder"
config.Tier0Feeder.pollInterval = 30
config.Tier0Feeder.tier0ConfigFile = "TIER0_CONFIG_FILE"
config.Tier0Feeder.specDirectory = "TIER0_SPEC_DIR"
config.Tier0Feeder.lfnBase = "TIER0_LFNBASE"

config.JobSubmitter.LsfPluginQueue = "cmsrepack"
config.JobSubmitter.LsfPluginResourceReq = "select[type==SLC5_64] rusage[pool=10000,mem=1800]"
config.JobSubmitter.LsfPluginJobGroup = "/groups/tier0/wmagent_testing"
config.JobSubmitter.LsfPluginBatchOutput = "None"

config.JobCreator.pollInterval = 30
config.JobSubmitter.pollInterval = 30
config.JobAccountant.pollInterval = 30

config.RetryManager.section_("PauseAlgo")
config.RetryManager.PauseAlgo.section_("default")
config.RetryManager.PauseAlgo.default.coolOffTime = retryAlgoParams
config.RetryManager.PauseAlgo.default.pauseCount = 3
config.RetryManager.plugins = {"default" : "PauseAlgo"}

config.ErrorHandler.maxRetries = 30
