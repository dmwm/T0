#!/bin/bash

BASE_DIR=/data/tier0
DEPLOY_DIR=$BASE_DIR/srv/wmagent
SPEC_DIR=$BASE_DIR/admin/Specs

TIER0_VERSION=2.2.1
TIER0_ARCH=slc7_amd64_gcc630

function echo_header {
    echo ''
    echo " *** $1 *** "
}

echo_header "Removing deploy dir \"$DEPLOY_DIR\""
rm -rf $DEPLOY_DIR
mkdir -p $DEPLOY_DIR

echo_header "Removing specs dir \"$SPEC_DIR\""
rm -rf $SPEC_DIR
mkdir -p $SPEC_DIR

cd $BASE_DIR
echo_header "deleting deployment dir \"deployment\""
rm -rf deployment
git clone https://github.com/dmwm/deployment.git
cd deployment

echo_header 'Deploying Tier0 WMAgent'
#Dirk's private repo deployment
#./Deploy -s prep -r comp=comp.hufnagel -A $TIER0_ARCH -t $TIER0_VERSION -R tier0@$TIER0_VERSION $DEPLOY_DIR tier0@$TIER0_VERSION
#./Deploy -s sw -r comp=comp.hufnagel -A $TIER0_ARCH -t $TIER0_VERSION -R tier0@$TIER0_VERSION $DEPLOY_DIR tier0@$TIER0_VERSION
#./Deploy -s post -r comp=comp.hufnagel -A $TIER0_ARCH -t $TIER0_VERSION -R tier0@$TIER0_VERSION $DEPLOY_DIR tier0@$TIER0_VERSION

#Usual deployment
./Deploy -s prep -r comp=comp -A $TIER0_ARCH -t $TIER0_VERSION -R tier0@$TIER0_VERSION $DEPLOY_DIR tier0@$TIER0_VERSION
./Deploy -s sw -r comp=comp -A $TIER0_ARCH -t $TIER0_VERSION -R tier0@$TIER0_VERSION $DEPLOY_DIR tier0@$TIER0_VERSION
./Deploy -s post -r comp=comp -A $TIER0_ARCH -t $TIER0_VERSION -R tier0@$TIER0_VERSION $DEPLOY_DIR tier0@$TIER0_VERSION

## global patch override
echo_header 'Applying general patches and cleaning t0ast'
$BASE_DIR/00_patches.sh 2>&1 > /dev/null

## clean database
$BASE_DIR/00_wipe_t0ast.sh 2>&1 > /dev/null

# needs secret file location and user certs
source $BASE_DIR/admin/env.sh

cd $DEPLOY_DIR/current

echo_header 'Initializing services / agent'
./config/tier0/manage activate-tier0
./config/tier0/manage start-services
./config/tier0/manage init-tier0
sleep 5

#
# mandatory configuration tweaks
#
#sed -i 's+TIER0_CONFIG_FILE+/data/tier0/admin/ProdOfflineConfiguration.py+' ./config/tier0/config.py
sed -i 's+TIER0_CONFIG_FILE+/data/tier0/admin/ReplayOfflineConfiguration.py+' ./config/tier0/config.py
sed -i 's+TIER0_SPEC_DIR+/data/tier0/admin/Specs+' ./config/tier0/config.py

# Real information for WMStats
sed -i "s+config.Agent.teamName = 'REPLACE_TEAM_NAME'+config.Agent.teamName = 'Tier0Replay'+" ./config/tier0/config.py
sed -i "s+config.Agent.contact = 'cms-comp-ops-workflow-team@cern.ch'+config.Agent.contact = 'cms-tier0-operations@cern.ch'+" ./config/tier0/config.py
#sed -i "s+OP EMAIL+Dirk.Hufnagel@cern.ch+g" ./config/tier0/config.py
#sed -i "s+wmagentalerts@gmail.com+Dirk.Hufnagel@cern.ch+g" ./config/tier0/config.py

#
# Use this team and not the default 
#
#sed -i "s+'team1,team2,cmsdataops'+'tier0production'+g" ./config/tier0/config.py
sed -i "s+'team1,team2,cmsdataops'+'tier0replay'+g" ./config/tier0/config.py

#
# configure retry settings
#
echo "config.RetryManager.PauseAlgo.default.coolOffTime = {'create': 10, 'job': 10, 'submit': 10}" >> ./config/tier0/config.py
#sed -i "s+ErrorHandler.pollInterval = 240+ErrorHandler.pollInterval = 30+g" ./config/tier0/config.py
#sed -i "s+RetryManager.pollInterval = 240+RetryManager.pollInterval = 30+g" ./config/tier0/config.py

#
# switch to ProcessingAlgo
#
#sed -i "s+config.RetryManager.plugins = {'default': 'PauseAlgo', 'Cleanup': 'SquaredAlgo', 'LogCollect': 'SquaredAlgo'}+config.RetryManager.plugins = {'default': 'ProcessingAlgo'}+g" ./config/tier0/config.py
#echo "config.RetryManager.section_('ProcessingAlgo')" >> ./config/tier0/config.py
#echo "config.RetryManager.ProcessingAlgo.section_('default')" >> ./config/tier0/config.py
#echo "config.RetryManager.ProcessingAlgo.default.coolOffTime = {'create': 10, 'job': 10, 'submit': 10}" >> ./config/tier0/config.py
#echo "config.RetryManager.ProcessingAlgo.default.closeoutPercentage = 95" >> ./config/tier0/config.py
#echo "config.RetryManager.ProcessingAlgo.default.guaranteedRetries = 4" >> ./config/tier0/config.py
#echo "config.RetryManager.ProcessingAlgo.default.minRetryTime = 1" >> ./config/tier0/config.py
#echo "config.RetryManager.ProcessingAlgo.default.maxRetryTime = 2" >> ./config/tier0/config.py

#
# configure DEBUG output
#
#sed -i "s+config.ErrorHandler.logLevel = 'INFO'+config.ErrorHandler.logLevel = 'DEBUG'+g" ./config/tier0/config.py
#sed -i "s+config.RetryManager.logLevel = 'INFO'+config.RetryManager.logLevel = 'DEBUG'+g" ./config/tier0/config.py
#sed -i "s+config.PhEDExInjector.logLevel = 'INFO'+config.PhEDExInjector.logLevel = 'DEBUG'+g" ./config/tier0/config.py
#sed -i "s+config.JobCreator.logLevel = 'INFO'+config.JobCreator.logLevel = 'DEBUG'+g" ./config/tier0/config.py

#
# configure shorter polling cyles
#
#echo 'config.ErrorHandler.pollInterval = 30' >> ./config/tier0/config.py
#echo 'config.RetryManager.pollInterval = 30' >> ./config/tier0/config.py
#echo 'config.DBS3Upload.pollInterval = 30' >> ./config/tier0/config.py
#echo 'config.PhEDExInjector.pollInterval = 30' >> ./config/tier0/config.py

#
# configure Tier0-Mode for PhEDEx
#
# Twiking Rucio configuration
sed -i "s+config.RucioInjector.listTiersToInject.*+config.RucioInjector.listTiersToInject = ['AOD', 'MINIAOD', 'NANOAOD', 'NANOAODSIM', 'RAW', 'FEVT', 'USER', 'ALCARECO', 'ALCAPROMPT', 'DQMIO','RAW-RECO']+" ./config/tier0/config.py
sed -i "s+config.RucioInjector.containerDiskRuleParams.*+config.RucioInjector.containerDiskRuleParams = {'lifetime': 15 * 24 * 60 * 60}+" ./config/tier0/config.py

#
# Set output datasets status to VALID in DBS
#
echo "config.DBS3Upload.datasetType = 'VALID'" >> ./config/tier0/config.py

#
# needed for LSF DQM uploads
#
#echo 'config.Tier0Feeder.dqmUploadProxy = "/afs/cern.ch/user/h/hufnagel/private/Certificates/dqmcert.pem"' >> ./config/tier0/config.py

#
# needed for conditions upload
#
echo "config.Tier0Feeder.serviceProxy = '/data/certs/serviceproxy-vocms001.pem'" >> ./config/tier0/config.py

#
# password for dropbox upload
#

HOME="/data/tier0/admin/"

if [ "x$WMAGENT_SECRETS_LOCATION" == "x" ]; then
    WMAGENT_SECRETS_LOCATION=$HOME/WMAgent.secrets;
fi
if [ -f $WMAGENT_SECRETS_LOCATION\.replay ]; then
    ln -s -f $WMAGENT_SECRETS_LOCATION\.replay $WMAGENT_SECRETS_LOCATION
fi
if [ ! -e $WMAGENT_SECRETS_LOCATION ]; then
    echo "Password file: $WMAGENT_SECRETS_LOCATION does not exist"
    echo "Either set WMAGENT_SECRETS_LOCATION to a valid file or check that $HOME/WMAgent.secrets exists"
    exit 1;
fi

DROPBOX_USER=`cat $WMAGENT_SECRETS_LOCATION | grep DROPBOX_USER | sed s/DROPBOX_USER=//`
DROPBOX_PASS=`cat $WMAGENT_SECRETS_LOCATION | grep DROPBOX_PASS | sed s/DROPBOX_PASS=//`

if [ "x$DROPBOX_USER" == "x" ] || [ "x$DROPBOX_PASS" == "x" ]; then
    echo "Secrets file doesn't contain DROPBOX_USER or DROPBOX_PASS";
    exit 1
fi

echo 'config.Tier0Feeder.dropboxuser = "'$DROPBOX_USER'"' >> ./config/tier0/config.py
echo 'config.Tier0Feeder.dropboxpass = "'$DROPBOX_PASS'"' >> ./config/tier0/config.py

#
# needed for passing notifications back to StorageManager
#
#echo 'config.Tier0Feeder.transferSystemBaseDir = "/data/tier0/sminject"' >> ./config/tier0/config.py

#
# upload PromptReco performance data
#
echo 'config.TaskArchiver.dashBoardUrl = "http://dashb-luminosity.cern.ch/dashboard/request.py/putluminositydata"' >> ./config/tier0/config.py
echo 'config.TaskArchiver.logLevel = "DEBUG"' >> ./config/tier0/config.py

#
# Workflow archive delay
#
#echo 'config.TaskArchiver.archiveDelayHours = 1' >> ./config/tier0/config.py
sed -i "s+config.TaskArchiver.archiveDelayHours = 24+config.TaskArchiver.archiveDelayHours = 1+" ./config/tier0/config.py

#
# Do not use WorkQueue
#
echo 'config.TaskArchiver.useWorkQueue = False' >> ./config/tier0/config.py

#
# Enable AgentStatusWatcher - site status automatic updated
#
echo "config.AgentStatusWatcher.enabled = False" >> ./config/tier0/config.py
echo "config.AgentStatusWatcher.onlySSB = False" >> ./config/tier0/config.py

#
# Increase ErrorHandler maxFailTime
#
echo "config.ErrorHandler.maxFailTime = 604800" >> ./config/tier0/config.py

#
# JobAccountant Repack Error Dataset settings
#
echo 'config.JobAccountant.maxAllowedRepackOutputSize = 24 * 1024 * 1024 * 1024' >> ./config/tier0/config.py

#
# Use SimpleCondorPlugin by default
#
echo 'config.BossAir.pluginNames = ["SimpleCondorPlugin"]' >> ./config/tier0/config.py

#
# Setting up sites
#

./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --cms-name=T2_CH_CERN --pnn=T2_CH_CERN --ce-name=T2_CH_CERN --pending-slots=20000 --running-slots=20000 --plugin=SimpleCondorPlugin
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Processing --pending-slots=10000 --running-slots=10000
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Merge --pending-slots=1000 --running-slots=1000
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Cleanup --pending-slots=1000 --running-slots=1000
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=LogCollect --pending-slots=1000 --running-slots=1000
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Skim --pending-slots=1 --running-slots=1
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Production --pending-slots=1 --running-slots=1
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Harvesting --pending-slots=1000 --running-slots=1000
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Express --pending-slots=3000 --running-slots=3000
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Repack --pending-slots=5000 --running-slots=5000

# Thresholds configurations
echo "config.AgentStatusWatcher.t1SitesCores = 12.5"  >> ./config/tier0/config.py

echo "config.AgentStatusWatcher.pendingSlotsTaskPercent = 30" >> ./config/tier0/config.py
echo "config.AgentStatusWatcher.pendingSlotsSitePercent = 40" >> ./config/tier0/config.py

echo "config.AgentStatusWatcher.runningExpressPercent = 25" >> ./config/tier0/config.py
echo "config.AgentStatusWatcher.runningRepackPercent = 10" >> ./config/tier0/config.py

#Configurable retry number for failing jobs before they go to paused
echo "config.RetryManager.PauseAlgo.section_('Express')" >> ./config/tier0/config.py
echo "config.RetryManager.PauseAlgo.Express.retryErrorCodes = { 8001: 0, 70: 0, 50513: 0, 50660: 0, 50661: 0, 71304: 0, 99109: 0, 99303: 0, 99400: 0, 8001: 0, 50115: 0 }" >> ./config/tier0/config.py
echo "config.RetryManager.PauseAlgo.section_('Processing')" >> ./config/tier0/config.py
echo "config.RetryManager.PauseAlgo.Processing.retryErrorCodes = { 8001: 0, 70: 0, 50513: 0, 50660: 0, 50661: 0, 71304: 0, 99109: 0, 99303: 0, 99400: 0, 8001: 0, 50115: 0 }" >> ./config/tier0/config.py
echo "config.RetryManager.PauseAlgo.section_('Repack')" >> ./config/tier0/config.py
echo "config.RetryManager.PauseAlgo.Repack.retryErrorCodes = { 8001: 0, 70: 0, 50513: 0, 50660: 0, 50661: 0, 71304: 0, 99109: 0, 99303: 0, 99400: 0, 8001: 0, 50115: 0 }" >> ./config/tier0/config.py
