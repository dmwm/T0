#!/usr/bin/env python
"""
Hopefully someone is going to refactor these scripts at some point.
"""
print("Checking replayWorkflowStatus")
import cx_Oracle
import time
import sys
import os
from jira import JIRA, JIRAError
from jiraReporting import JiraReporting


# Initial configuration
# Authentication credentials
jira_cookie = '/data/tier0/jenkins/jiraBiscuit.txt'

jira_url = 'https://its.cern.ch/jira'
headers = {'Accept': 'application/json'}
proxy = '/data/certs/proxy.pem'

# CMSWeb and JIRA instances
jira_project_prod = "CMSTZ"
jira_project_test = "CMSTZDEV"

#Email configuration
mail_address = "cms-tier0-monitoring-alerts@cern.ch"
mail_subject = "Jenkins automatic replay"

#Jira watchers list. Should be updated with present T0 team
watchers = ['anquinte', 'vjankaus', 'yulee']
labels = ['Tier0_Replays']
print("run t0 workflow replay")

def getT0astCreds():
    print("getT0astCreds")
    home="/data/tier0/admin/"
    fileName="WMAgent.secrets"
    ORACLE_USER=""
    ORACLE_PASS=""
    ORACLE_TNS=""
    try:
        with open(home+fileName) as f:
            for line in f:
                if line.startswith("ORACLE_USER"):
                    ORACLE_USER=line.strip().split("=")[-1]
                elif line.startswith("ORACLE_PASS"):
                    ORACLE_PASS=line.strip().split("=")[-1]
                elif line.startswith("ORACLE_TNS"):
                    ORACLE_TNS=line.strip().split("=")[-1]
    except IOError:
        print("Could not read file:", home+fileName)
    return [ORACLE_USER,ORACLE_PASS,ORACLE_TNS]

#check the number of workflows by type Repack/Express
def getWorkflowCount(creds, workflowName):
    print("getWorkflowCount",)
    dbconn = cx_Oracle.connect(creds[0], creds[1], creds[2])
    cursor = dbconn.cursor() 
    #Get a number of workflows in progress 
    query = "SELECT DISTINCT name FROM dbsbuffer_workflow WHERE completed = 0 AND name like '%" + workflowName +"%'"
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)
    return len(result)

#check the number of filesets on DB
def getFilesets(creds):
    print("getFilesets")
    dbconn = cx_Oracle.connect(creds[0], creds[1], creds[2])
    cursor = dbconn.cursor()
    #Get a number of filesets
    query = "SELECT COUNT(*) FROM wmbs_fileset"
    cursor.execute(query)
    result = cursor.fetchall()[0]
    return result[0]

def getPaused(creds):
    print("getPaused")
    dbconn = cx_Oracle.connect(creds[0], creds[1], creds[2])
    cursor = dbconn.cursor() 
    #Get a number of paused jobs
    query =  "SELECT id, name, cache_dir FROM wmbs_job WHERE state = (SELECT id FROM wmbs_job_state WHERE name = 'jobpaused')"
    #print(query)
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)
    return len(result)

def main():
    """
    _main_
    Script's main function:
        check until all Express or Repack workflows are done.
    """
    jiraReporting = JiraReporting()
    jira_instance = jira_project_test

    #load cookies
    cj = jiraReporting.loadCookies(jira_cookie)

    #Get the proxy
    proxy_info = jiraReporting.getProxy(proxy)

    #Initialize JIRA instance 
    jira = JIRA(jira_url)
    jira._session.cookies = cj

    print(sys.argv)
    if len(sys.argv) == 7:
        print("set jira environment")
        buildNumber = sys.argv[1]
        hostName = os.popen('hostname').read().rstrip()
        print(hostName)
        jobname = sys.argv[2]
        prTitle = sys.argv[3]
        prMessage = sys.argv[4]
        prLink = sys.argv[5]
        buildurl = sys.argv[6]

        print(buildNumber)
        print(prTitle)
        print(prMessage)
        print(prLink)
        ticketDescription = """Configuration for the replay is available at: {}
                           The information of this build can be found at {}.
                           """.format(prLink,buildurl)
        subject = "Tier0_REPLAY v{} {} on {}. {}".format(str(buildNumber),jobname,hostName,prTitle)
        #create a new JIRA issue
        newIssue = jiraReporting.createJiraTicket(jira, jira_instance, subject, ticketDescription, labels, watchers)
        firstComment = jiraReporting.addJiraComment(jira, jira_instance, newIssue, "The replay has started. Its progress will be reported here.")

    # To stop sending emails, comment out the line below
    # send an email with the summary of Jira issues
    #sendEmailAlert(tickets, sources, extraComment)

    creds=getT0astCreds()
    repackWorkflowCount = 1
    expressWorkflowCount = 1
    processing = True
    expressProcessing = True
    repackProcessing = True
    while processing:
        filesetCount = getFilesets(creds)
        if filesetCount == 0:
            try:
                jiraReporting.addJiraComment(jira, jira_instance, newIssue, "All filesets were closed.")
                print("All filesets were closed.")
            except Exception as e:
                print(e)
                print("Unable to comment JIRA issue 0.")
        pausedCount = getPaused(creds)
        if pausedCount != 0:
            print("There are {} paused jobs in the replay.".format(pausedCount))
            try:
                jiraReporting.addJiraComment(jira, jira_instance, newIssue, "*There are {} paused jobs in the replay.*".format(pausedCount))
                print("*There are {} paused jobs in the replay.*".format(pausedCount))
                sys.exit(1)
            except Exception as e:
                print(e)
                print("Unable to comment JIRA issue 1.")
        if filesetCount == 0 and pausedCount == 0:
            try:
                jiraReporting.addJiraComment(jira, jira_instance, newIssue, "*There were NO paused jobs in the replay.*")
                jiraReporting.addJiraComment(jira, jira_instance, newIssue, "*Replay was successful.*")
                sys.exit(0)
            except Exception as e:
                print(e.message, e.args)
                print("There were errors when the replay has already finished.")
                print("Unable to comment JIRA issue 2.")
        if repackProcessing:
            print("Checking Repack workflows... repackworkflowcount {}".format(repackWorkflowCount))
            if repackWorkflowCount > 0:
                repackWorkflowCount = getWorkflowCount(creds, "Repack")
            else:
                try:
                    jiraReporting.addJiraComment(jira, jira_instance, newIssue, "All Repack workflows were processed.")
                    print("All Repack workflows were processed.")
                except Exception as e:
                    print(e)
                    print("Unable to comment JIRA issue 3.")
                repackProcessing = False
        if expressProcessing:
            print("Checking Express workflows...")
            if expressWorkflowCount > 0:
                expressWorkflowCount = getWorkflowCount(creds, "Express")
            else:
                try:
                    jiraReporting.addJiraComment(jira, jira_instance, newIssue, "All Express workflows were processed.")
                    print("All Express workflows were processed.")
                except Exception as e:
                    print(e)
                    print("Unable to comment JIRA issue 4.")
                expressProcessing = False
        time.sleep(60)

if __name__ == "__main__":
    main()
