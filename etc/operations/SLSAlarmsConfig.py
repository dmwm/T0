from WMCore.Configuration import Configuration

config = Configuration()

# General configuration
config.section_("Settings")
config.Settings.xmlDir = "/afs/cern.ch/user/c/cmsprod/www/sls"

# Late workflows alarm
config.section_("cmst0_late_workflows")
config.cmst0_late_workflows.section_("WorkflowTimeouts")
config.cmst0_late_workflows.WorkflowTimeouts.section_("Express")
config.cmst0_late_workflows.WorkflowTimeouts.Express.states = ["Closed", "Merge", "Harvesting", "ProcessingDone"]
config.cmst0_late_workflows.WorkflowTimeouts.Express.Closed = 3
config.cmst0_late_workflows.WorkflowTimeouts.Express.Merge = 2
config.cmst0_late_workflows.WorkflowTimeouts.Express.Harvesting = 1
config.cmst0_late_workflows.WorkflowTimeouts.Express.ProcessingDone = 2
config.cmst0_late_workflows.WorkflowTimeouts.section_("Repack")
config.cmst0_late_workflows.WorkflowTimeouts.Repack.states = ["Closed", "Merge", "ProcessingDone"]
config.cmst0_late_workflows.WorkflowTimeouts.Repack.Closed = 4
config.cmst0_late_workflows.WorkflowTimeouts.Repack.Merge = 4
config.cmst0_late_workflows.WorkflowTimeouts.Repack.ProcessingDone = 52
config.cmst0_late_workflows.WorkflowTimeouts.section_("PromptReco")
config.cmst0_late_workflows.WorkflowTimeouts.PromptReco.states = ["Closed", "AlcaSkim",
                                                                "Merge", "Harvesting",
                                                                "ProcessingDone"]
config.cmst0_late_workflows.WorkflowTimeouts.PromptReco.Closed = 14
config.cmst0_late_workflows.WorkflowTimeouts.PromptReco.AlcaSkim = 4
config.cmst0_late_workflows.WorkflowTimeouts.PromptReco.Merge = 4
config.cmst0_late_workflows.WorkflowTimeouts.PromptReco.Harvesting = 1
config.cmst0_late_workflows.WorkflowTimeouts.PromptReco.ProcessingDone = 1
config.cmst0_late_workflows.runBlacklist = ["000000"]
config.cmst0_late_workflows.xmlFile = "cmst0_late_workflows.xml"
config.cmst0_late_workflows.section_("Intervention")
config.cmst0_late_workflows.Intervention.startTime = "2012-12-06T23:00:00"
config.cmst0_late_workflows.Intervention.duration = 2
config.cmst0_late_workflows.Intervention.message = "Test intervention"

# Backlog alarm
config.section_("cmst0_backlog_wma")
config.cmst0_backlog_wma.xmlFile = "cmst0-backlog-wma.xml"
config.cmst0_backlog_wma.express = 2000
config.cmst0_backlog_wma.repack = 50
config.cmst0_backlog_wma.promptreco = 15000
config.cmst0_backlog_wma.section_("Intervention")
config.cmst0_backlog_wma.Intervention.startTime = "2012-12-05T23:00:00"
config.cmst0_backlog_wma.Intervention.duration = 2
config.cmst0_backlog_wma.Intervention.message = "Test intervention"


