#!/bin/bash

CONFIGURATION_FILE=/data/tier0/admin/ReplayOfflineConfiguration.py
sed -i 's+TIER0_CONFIG_FILE+'"$CONFIGURATION_FILE"'+' "$config/config.py"
sed -i "s+config.Agent.teamName = 'REPLACE_TEAM_NAME'+config.Agent.teamName = '"$TEAMNAME"'+" "$config/config.py"
sed -i "s+config.Agent.contact = 'cms-comp-ops-workflow-team@cern.ch'+config.Agent.contact = 'cms-tier0-operations@cern.ch'+" "$config/config.py"
sed -i "s+'team1,team2,cmsdataops'+'tier0replay'+g" "$config/config.py"
sed -i "s+config.RucioInjector.containerDiskRuleParams.*+config.RucioInjector.containerDiskRuleParams = {'lifetime': 7 * 24 * 60 * 60}+" "$config/config.py"
echo "config.RucioInjector.blockRuleParams = {'lifetime': 7 * 24 * 60 * 60}" >> "$config/config.py"
sed -i "s+config.RucioInjector.metaDIDProject.*+config.RucioInjector.metaDIDProject = 'Test'+" "$config/config.py"
echo "config.RucioInjector.blockDeletionDelayHours = 2" >> $config/config.py
echo "config.DBS3Upload.datasetType = 'VALID'" >> $config/config.py
echo "config.Tier0Feeder.serviceProxy = '$WMA_DEPLOY_DIR/certs/myproxy.pem'" >> $config/config.py
echo 'config.TaskArchiver.dashBoardUrl = "http://dashb-luminosity.cern.ch/dashboard/request.py/putluminositydata"' >> $config/config.py
sed -i "s+config.DBS3Upload.uploaderName = 'WMAgent'+config.DBS3Upload.uploaderName = 'T0Replay'+g" "$config/config.py"
#Overwrite ErrorHandler to avoid jobs going to ensure T0 jobs can always be retried
sed -i "s/config.ErrorHandler.maxFailTime.*/config.ErrorHandler.maxFailTime=601200/g" "$config/config.py"
sed -i "s+config.RucioInjector.listTiersToInject.*+config.RucioInjector.listTiersToInject = ['AOD', 'MINIAOD', 'NANOAOD', 'NANOAODSIM', 'RAW', 'FEVT', 'USER', 'ALCARECO', 'ALCAPROMPT','DQMIO','RAW-RECO']+" "$config/config.py"

##### ONLY IN REPLAY #####
sed -i "s/config.RetryManager.plugins.*/config.RetryManager.plugins={'default': 'PauseAlgo', 'Cleanup': 'PauseAlgo', 'LogCollect': 'PauseAlgo'}/g" "$config/config.py"
sed -i "s/config.ErrorHandler.maxRetries.*/config.ErrorHandler.maxRetries={'default': 30, 'Cleanup': 30, 'LogCollect': 30}/g" "$config/config.py"
##### ONLY IN REPLAY #####

# Enable AgentStatusWatcher - site status automatic updated
sed -i "s+config.AgentStatusWatcher.ignoreDisks.*+config.AgentStatusWatcher.ignoreDisks = [ '/cvmfs/cvmfs-config.cern.ch', '/cvmfs/cms.cern.ch', '/eos/cms', '/cvmfs/cms-ib.cern.ch', '/cvmfs/patatrack.cern.ch' ]+" "$config/config.py"

# password for dropbox upload

DROPBOX_USER=`cat $WMA_SECRETS_FILE | grep DROPBOX_USER | sed s/DROPBOX_USER=//`
DROPBOX_PASS=`cat $WMA_SECRETS_FILE | grep DROPBOX_PASS | sed s/DROPBOX_PASS=//`

if [ "x$DROPBOX_USER" == "x" ] || [ "x$DROPBOX_PASS" == "x" ]; then
    echo "Secrets file doesn't contain DROPBOX_USER or DROPBOX_PASS";
    exit 1
fi

echo 'config.Tier0Feeder.dropboxuser = "'$DROPBOX_USER'"' >> $config/config.py
echo 'config.Tier0Feeder.dropboxpass = "'$DROPBOX_PASS'"' >> $config/config.py

##### ONLY IN PROD #####
#echo "config.RucioInjector.blockDeletionDelayHours = 168" >> ./config/tier0/config.py
#echo 'config.BossAir.pluginNames = ["SimpleCondorPlugin"]' >> ./config/tier0/config.py
#echo 'config.JobAccountant.maxAllowedRepackOutputSize = 24 * 1024 * 1024 * 1024' >> ./config/tier0/config.py
#echo "config.AgentStatusWatcher.runningExpressPercent = 25" >> ./config/tier0/config.py
#echo "config.AgentStatusWatcher.runningRepackPercent = 10" >> ./config/tier0/config.py
#echo 'config.TaskArchiver.archiveDelayHours = 2190' >> $config.py
##### ONLY IN PROD #####