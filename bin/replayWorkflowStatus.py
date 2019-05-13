#!/usr/bin/env python
"""
"""

import cx_Oracle
import time
import sys

def getT0astCreds():

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
    
    dbconn = cx_Oracle.connect(creds[0], creds[1], creds[2])
    cursor = dbconn.cursor() 
    #Get a number of workflows in progress 
    query = "SELECT DISTINCT name FROM dbsbuffer_workflow WHERE completed = 0 AND name like '%" + workflowName +"%'"
    cursor.execute(query)
    result = cursor.fetchall()
    return len(result)

#check the number of filesets on DB
def getFilesets(creds):

    dbconn = cx_Oracle.connect(creds[0], creds[1], creds[2])
    cursor = dbconn.cursor()
    #Get a number of filesets
    query = "SELECT COUNT(*) FROM wmbs_fileset"
    cursor.execute(query)
    result = cursor.fetchall()[0]
    return result[0]

def getPaused(creds):
    
    dbconn = cx_Oracle.connect(creds[0], creds[1], creds[2])
    cursor = dbconn.cursor() 
    #Get a number of paused jobs
    query =  "SELECT id, name, cache_dir FROM wmbs_job WHERE state = (SELECT id FROM wmbs_job_state WHERE name = 'jobpaused')"
    #print(query)
    cursor.execute(query)
    result = cursor.fetchall()
    #print(len(result))
    return len(result)

def main():
    """
    _main_
    Script's main function:
        check until all Express or Repack workflows are done.
    """
    workflowName = sys.argv[1]
    creds=getT0astCreds()
    workflowCount = 1
    processing = True
    while processing:
        if workflowName == "Fileset":
            filesetCount = getFilesets(creds)
            if filesetCount == 0:
                sys.exit(0)
        elif workflowName == "Paused":
            pausedCount = getPaused(creds)
            if pausedCount != 0:
                sys.exit(1)
            else:
                filesetCount = getFilesets(creds)
                if filesetCount == 0:
                    sys.exit(0)
        else:
            if workflowCount > 0:
                workflowCount = getWorkflowCount(creds, workflowName)
            else:
                sys.exit(0)
        time.sleep(10)


if __name__ == "__main__":
    main()