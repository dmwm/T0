from WMCore.Configuration import Configuration

config = Configuration()

# General configuration
config.section_("Settings")
config.Settings.xmlDir = "/data/tier0/sls"

# Late workflows alarm
config.section_("cmst0_late_workflows")
config.cmst0_late_workflows.section_("WorkflowTimeouts")
config.cmst0_late_workflows.WorkflowTimeouts.section_("Express")
config.cmst0_late_workflows.WorkflowTimeouts.Express.states = ["Closed", "Merge", "Harvesting", "ProcessingDone"]
config.cmst0_late_workflows.WorkflowTimeouts.Express.Closed = 3
config.cmst0_late_workflows.WorkflowTimeouts.Express.Merge = 2
config.cmst0_late_workflows.WorkflowTimeouts.Express.Harvesting = 6
config.cmst0_late_workflows.WorkflowTimeouts.Express.ProcessingDone = 12
config.cmst0_late_workflows.WorkflowTimeouts.section_("Repack")
config.cmst0_late_workflows.WorkflowTimeouts.Repack.states = ["Closed", "Merge", "ProcessingDone"]
config.cmst0_late_workflows.WorkflowTimeouts.Repack.Closed = 8
config.cmst0_late_workflows.WorkflowTimeouts.Repack.Merge = 4
config.cmst0_late_workflows.WorkflowTimeouts.Repack.ProcessingDone = 96
config.cmst0_late_workflows.WorkflowTimeouts.section_("PromptReco")
config.cmst0_late_workflows.WorkflowTimeouts.PromptReco.states = ["Closed", "AlcaSkim",
                                                                "Merge", "Harvesting",
                                                                "ProcessingDone"]
config.cmst0_late_workflows.WorkflowTimeouts.PromptReco.Closed = 18
config.cmst0_late_workflows.WorkflowTimeouts.PromptReco.AlcaSkim = 4
config.cmst0_late_workflows.WorkflowTimeouts.PromptReco.Merge = 4
config.cmst0_late_workflows.WorkflowTimeouts.PromptReco.Harvesting = 6
config.cmst0_late_workflows.WorkflowTimeouts.PromptReco.ProcessingDone = 12
config.cmst0_late_workflows.RunBlacklist = ["000000"]
config.cmst0_late_workflows.xmlFile = "cmst0_late_workflows.xml"
config.cmst0_late_workflows.section_("Intervention")
config.cmst0_late_workflows.Intervention.startTime = "2015-01-31T23:00:00"
config.cmst0_late_workflows.Intervention.duration = 2
config.cmst0_late_workflows.Intervention.message = "Test intervention"

# Backlog alarm
config.section_("cmst0_backlog_wma")
config.cmst0_backlog_wma.xmlFile = "cmst0_backlog_wma.xml"
config.cmst0_backlog_wma.Express = 3120
config.cmst0_backlog_wma.Repack = 780
config.cmst0_backlog_wma.PromptReco = 15000
config.cmst0_backlog_wma.section_("Intervention")
config.cmst0_backlog_wma.Intervention.startTime = "2015-01-31T23:00:00"
config.cmst0_backlog_wma.Intervention.duration = 2
config.cmst0_backlog_wma.Intervention.message = "Test intervention"

# Long jobs alarm
config.section_("cmst0_long_jobs")
config.cmst0_long_jobs.xmlFile = "cmst0_long_jobs.xml"
config.cmst0_long_jobs.section_("Thresholds")
config.cmst0_long_jobs.Thresholds.section_("Pending")
config.cmst0_long_jobs.Thresholds.Pending.Express = 1
config.cmst0_long_jobs.Thresholds.Pending.Repack = 1
config.cmst0_long_jobs.Thresholds.Pending.Merge = 1
config.cmst0_long_jobs.Thresholds.Pending.Processing = 6
config.cmst0_long_jobs.Thresholds.section_("Running")
config.cmst0_long_jobs.Thresholds.Running.Express = 4
config.cmst0_long_jobs.Thresholds.Running.Repack = 8
config.cmst0_long_jobs.Thresholds.Running.Merge = 4
config.cmst0_long_jobs.Thresholds.Running.Harvesting = 6
config.cmst0_long_jobs.Thresholds.Running.Processing = 18
config.cmst0_long_jobs.Thresholds.Running.LogCollect = 24
config.cmst0_long_jobs.Thresholds.Running.Cleanup = 24
config.cmst0_long_jobs.RunBlacklist = ["000000"]
config.cmst0_long_jobs.section_("Intervention")
config.cmst0_long_jobs.Intervention.startTime = "2015-01-31T23:00:00"
config.cmst0_long_jobs.Intervention.duration = 2
config.cmst0_long_jobs.Intervention.message = "Test intervention"

# Paused jobs alarm
config.section_("cmst0_paused_jobs")
config.cmst0_paused_jobs.xmlFile = "cmst0_paused_jobs.xml"
config.cmst0_paused_jobs.RunBlacklist = ["000000"]
config.cmst0_paused_jobs.section_("Intervention")
config.cmst0_paused_jobs.Intervention.startTime = "2015-01-31T23:00:00"
config.cmst0_paused_jobs.Intervention.duration = 2
config.cmst0_paused_jobs.Intervention.message = "Test intervention"




