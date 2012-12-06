#!/usr/bin/env python

from WMCore.Configuration import loadConfigurationFile
from WMCore.Database.CMSCouch import Database
from string import Template
import os
import time

# Load/set configuration :
config = loadConfigurationFile(os.environ["WMAGENT_CONFIG"])
alarmConfigPath = os.path.join(os.environ.get("SLS_CONFIG") or
                               os.environ["T0_ROOT"], 'etc/operations/SLSAlarmsConfig.py')
alarmConfig = loadConfigurationFile(alarmConfigPath)
xmlFile = getattr(alarmConfig.cmst0_backlog_wma, "xmlFile", None) or "cmst0_backlog_wma.xml"
slsXml = os.path.join(alarmConfig.Settings.xmlDir, xmlFile)

# Getting what we need from configuration
couchURL = config.JobStateMachine.couchurl
jobsDatabase = config.JobStateMachine.couchDBName + "/jobs"

jobsDB = Database(jobsDatabase, couchURL)

# This is the same as (example) :
# http://vocms15.cern.ch:5984/wmagent_jobdump%2Fjobs/_design/JobDump/_view/createdJobsByWorkflowName?group_level=1
rows = jobsDB.loadView("JobDump", "createdJobsByWorkflowName", {"group_level" : 1})

# This will store how much created jobs we have on each type, created means in the system but still not submitted
jobCounts = {
    "Express" : 0,
    "Repack" : 0,
    "PromptReco" : 0
}

for row in rows['rows']:
    workflow = row['key'][0]
    workflowType = workflow.split("_")[0]
    createdJobs = row['value']

    jobCounts[workflowType] += createdJobs        

# Here comes the TH logic, very simple in the beginning
availability = 100
for workflowType in jobCounts:
    limit = getattr(alarmConfig.cmst0_backlog_wma, workflowType.lower())
    if jobCounts[workflowType] > limit:
        availability = 0

interventionInfo = {}
if hasattr(alarmConfig.cmst0_backlog_wma, "Intervention"):
    startTime = alarmConfig.cmst0_backlog_wma.Intervention.startTime
    duration = alarmConfig.cmst0_backlog_wma.Intervention.duration
    message = alarmConfig.cmst0_backlog_wma.Intervention.message

    # Check that the intervention is present or in the future
    structStartTime = time.strptime(startTime, "%Y-%m-%dT%H:%M:%S")
    startTimeSeconds = time.mktime(structStartTime)
    if (startTimeSeconds + duration * 3600) >= time.time():
        interventionInfo = {'startTime' : startTime,
                            'duration' : duration,
                            'message' : message}
intervention = ""
if interventionInfo:
    inteventionTemplate = """        <interventions>
        <intervention start="{startTime}" length="PT{duration}H">
            {message}
        </intervention>
    </interventions>"""

    intervention = inteventionTemplate.format(**interventionInfo)

timezone = str(int(-time.timezone / 3600)).zfill(2)
timestamp = time.strftime("%Y-%m-%dT%H:%M:%S+")
timestamp += "%s:00" % timezone
xmlValues = {         
		"availability"  : availability,
		"timestamp"     : timestamp,
		"promptreco_count": jobCounts["PromptReco"],
		"express_count"	: jobCounts["Express"],
		"repack_count"	: jobCounts["Repack"],
        "intervention"  : intervention
} 
            

template = Template("""<?xml version="1.0" encoding="utf-8"?>
       <serviceupdate xmlns="http://sls.cern.ch/SLS/XML/update">
               <id>CMST0-backlog-wma</id>
               <availability>$availability</availability>
               <timestamp>$timestamp</timestamp>
               <data>
                       <numericvalue name="promptreco_count" desc="Backlogged PromptReco">$promptreco_count</numericvalue>
                       <numericvalue name="repack_count" desc="Backlogged Repack">$repack_count</numericvalue>
                       <numericvalue name="express_count" desc="Backlogged Express">$express_count</numericvalue>
               </data>
               $intervention
       </serviceupdate> """)

xmlUpdated = template.safe_substitute(xmlValues)
xml = open(slsXml,'w')
xml.write(xmlUpdated)
xml.close()
