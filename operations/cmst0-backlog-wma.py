#!/usr/bin/env python

from WMCore.Configuration import loadConfigurationFile
from WMCore.Database.CMSCouch import Database
from string import Template
import os
import time

# Load/set configuration :
config = loadConfigurationFile(os.environ["WMAGENT_CONFIG"])
slsXml = "/afs/cern.ch/user/c/cmsprod/www/sls/cmst0-backlog-wma.xml"

# Getting what we need from configuration
couchURL = config.WMBSService.views.active.wmbs.couchConfig.couchURL
couchURL = "http://vocms15.cern.ch:5984"
jobsDatabase = config.WMBSService.views.active.wmbs.couchConfig.jobDumpDBName+"/jobs"

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
if jobCounts["PromptReco"] > 15000 or jobCounts["Express"]  > 2000 or jobCounts["Repack"] > 500:
	availability = 0
else: 
	availability = 100 


timestamp = time.strftime("%Y-%m-%dT%H:%M:%S+02:00") 
xmlValues = {         
		"availability"  : availability,
		"timestamp"     : timestamp,
		"promptreco_count": jobCounts["PromptReco"],
		"express_count"	: jobCounts["Express"],
		"repack_count"	: jobCounts["Repack"]
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
       </serviceupdate> """)

xmlUpdated = template.safe_substitute(xmlValues)
xml = open(slsXml,'w')
xml.write(xmlUpdated)
xml.close()
