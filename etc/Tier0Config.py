# pylint: skip-file
config.component_('Tier0Feeder')
config.Tier0Feeder.namespace = "T0Component.Tier0Feeder.Tier0Feeder"
config.Tier0Feeder.componentDir = config.General.workDir + "/Tier0Feeder"
config.Tier0Feeder.pollInterval = 30
config.Tier0Feeder.tier0ConfigFile = "TIER0_CONFIG_FILE"
config.Tier0Feeder.specDirectory = "/data/tier0/admin/Specs"
config.Tier0Feeder.requestDBName = "t0_request_local"
config.Tier0Feeder.serviceProxy = '/data/tier0/WMAgent.venv3/certs/myproxy.pem'

config.JobAccountant.pollInterval = 30
config.JobAccountant.maxAllowedRepackOutputSize = 24 * 1024 * 1024 * 1024

config.JobArchiver.handleInjected = False

config.JobCreator.pollInterval = 30

config.JobSubmitter.LsfPluginQueue = "cmsrepack"
config.JobSubmitter.LsfPluginResourceReq = "select[type==SLC5_64] rusage[pool=10000,mem=1800]"
config.JobSubmitter.LsfPluginJobGroup = "/groups/tier0/wmagent_testing"
config.JobSubmitter.LsfPluginBatchOutput = "None"
config.JobSubmitter.pollInterval = 30

config.RetryManager.section_("PauseAlgo")
config.RetryManager.PauseAlgo.section_("default")
config.RetryManager.PauseAlgo.default.pauseCount = 3
config.RetryManager.PauseAlgo.default.coolOffTime = {'create': 10, 'job': 10, 'submit': 10}
config.RetryManager.plugins = {"default" : "PauseAlgo", "Cleanup" : "SquaredAlgo", "LogCollect" : "SquaredAlgo"}

config.RetryManager.PauseAlgo.section_('Express')
config.RetryManager.PauseAlgo.Express.retryErrorCodes = { 70: 0, 50660: 0, 50661: 0, 50664: 0, 71304: 0 }
config.RetryManager.PauseAlgo.section_('Processing')
config.RetryManager.PauseAlgo.Processing.retryErrorCodes = { 70: 0, 50660: 0, 50661: 1, 50664: 0, 71304: 1 }
config.RetryManager.PauseAlgo.section_('Repack')
config.RetryManager.PauseAlgo.Repack.retryErrorCodes = { 70: 0, 50660: 0, 50661: 0, 50664: 0, 71304: 0 }

config.ErrorHandler.maxRetries = {"default" : 30, "Cleanup" : 2, "LogCollect" : 2}

config.TaskArchiver.useReqMgrForCompletionCheck = False
config.TaskArchiver.dashBoardUrl = "http://dashb-luminosity.cern.ch/dashboard/request.py/putluminositydata"
config.TaskArchiver.logLevel = "DEBUG"
config.TaskArchiver.archiveDelayHours = 2190
config.TaskArchiver.useWorkQueue = False

config.DBS3Upload.primaryDatasetType = "data"
config.DBS3Upload.datasetType = 'VALID'

config.DBSInterface.primaryDatasetType = "data"

config.AnalyticsDataCollector.pluginName = "Tier0Plugin"

config.AgentStatusWatcher.t1SitesCores = 12.5
config.AgentStatusWatcher.pendingSlotsTaskPercent = 30
config.AgentStatusWatcher.pendingSlotsSitePercent = 40
config.AgentStatusWatcher.runningExpressPercent = 25
config.AgentStatusWatcher.runningRepackPercent = 10
config.AgentStatusWatcher.enabled = False
config.AgentStatusWatcher.onlySSB = False

config.RucioInjector.blockRuleParams = {}
config.RucioInjector.blockDeletionDelayHours = 168
config.RucioInjector.useDsetReplicaDeep = True

config.BossAir.pluginNames = ["SimpleCondorPlugin"]

