#!/bin/bash
confirm_deploy=""
replay_nodes=("vocms0500.cern.ch" "vocms047.cern.ch" "vocms001.cern.ch" "vocms015.cern.ch" "vocms0501.cern.ch" "vocms0502.cern.ch")
is_production_node=1
for node in ${replay_nodes[@]}; do
	if [ "$node" == `hostname` ]
	then
		is_production_node=0
		break	
	fi
done

if [ $is_production_node -eq 1 ]
then
	echo "Are you sure you wish to deploy the production node `hostname`? (y/n)"
	read confirm_deploy
else
	confirm_deploy="y"
fi


if [ "$confirm_deploy" != "y" ]
then
	echo "Deployment aborted"
	exit
fi

BASE_DIR=/data/tier0
DEPLOY_DIR=$BASE_DIR/srv/wmagent
SPEC_DIR=$BASE_DIR/admin/Specs

TIER0_VERSION=3.1.5
TIER0_ARCH=slc7_amd64_gcc630
DEPLOY_TAG=HG2402a

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
git clone https://github.com/dmwm/deployment.git  --branch $DEPLOY_TAG
cd deployment

#Patch to test deployment adjustments
#curl https://patch-diff.githubusercontent.com/raw/dmwm/deployment/pull/893.patch| patch -d ./ -p1

echo_header 'Deploying Tier0 WMAgent'
#Dirk's private repo deployment
#./Deploy -s prep -r comp=comp.hufnagel -A $TIER0_ARCH -t $TIER0_VERSION -R tier0@$TIER0_VERSION $DEPLOY_DIR tier0@$TIER0_VERSION
#./Deploy -s sw -r comp=comp.hufnagel -A $TIER0_ARCH -t $TIER0_VERSION -R tier0@$TIER0_VERSION $DEPLOY_DIR tier0@$TIER0_VERSION
#./Deploy -s post -r comp=comp.hufnagel -A $TIER0_ARCH -t $TIER0_VERSION -R tier0@$TIER0_VERSION $DEPLOY_DIR tier0@$TIER0_VERSION

#German deployment
#./Deploy -s prep -r comp=comp.ggiraldo -A $TIER0_ARCH -t $TIER0_VERSION -R tier0@$TIER0_VERSION $DEPLOY_DIR tier0@$TIER0_VERSION
#./Deploy -s sw -r comp=comp.ggiraldo -A $TIER0_ARCH -t $TIER0_VERSION -R tier0@$TIER0_VERSION $DEPLOY_DIR tier0@$TIER0_VERSION
#./Deploy -s post -r comp=comp.ggiraldo -A $TIER0_ARCH -t $TIER0_VERSION -R tier0@$TIER0_VERSION $DEPLOY_DIR tier0@$TIER0_VERSION

#JamadoVa deployment
#./Deploy -s prep -r comp=comp.jamadova -A $TIER0_ARCH -t $TIER0_VERSION -R tier0@$TIER0_VERSION $DEPLOY_DIR tier0@$TIER0_VERSION
#./Deploy -s sw -r comp=comp.jamadova -A $TIER0_ARCH -t $TIER0_VERSION -R tier0@$TIER0_VERSION $DEPLOY_DIR tier0@$TIER0_VERSION
#./Deploy -s post -r comp=comp.jamadova -A $TIER0_ARCH -t $TIER0_VERSION -R tier0@$TIER0_VERSION $DEPLOY_DIR tier0@$TIER0_VERSION

#Usual deployment
#echo '---- Pre-deployment:'
./Deploy -s prep -r comp=comp -A $TIER0_ARCH -t $TIER0_VERSION -R tier0@$TIER0_VERSION $DEPLOY_DIR tier0@$TIER0_VERSION
#echo '---- Deployment:'
./Deploy -s sw -r comp=comp -A $TIER0_ARCH -t $TIER0_VERSION -R tier0@$TIER0_VERSION $DEPLOY_DIR tier0@$TIER0_VERSION
#echo '---- Post-deployment:'
./Deploy -s post -r comp=comp -A $TIER0_ARCH -t $TIER0_VERSION -R tier0@$TIER0_VERSION $DEPLOY_DIR tier0@$TIER0_VERSION

## global patch override
echo_header 'Applying general patches and cleaning t0ast'
$BASE_DIR/00_patches.sh 2>&1 > /dev/null

# needs location of user certs
source $BASE_DIR/admin/env.sh

# Override secrets file location for replays
export WMAGENT_SECRETS_LOCATION=$BASE_DIR/admin/WMAgent.secrets.replay

## clean database
$BASE_DIR/00_wipe_t0ast.sh 2>&1 > /dev/null

cd $DEPLOY_DIR/current

echo_header 'Initializing services / agent'
./config/tier0/manage activate-tier0
./config/tier0/manage start-services
./config/tier0/manage init-tier0
sleep 5
echo '-------------------------------------'
echo $TIER0_CONFIG_FILE
#
# mandatory configuration tweaks
#
#sed -i 's+TIER0_CONFIG_FILE+/data/tier0/admin/ProdOfflineConfiguration.py+' ./config/tier0/config.py
sed -i 's+TIER0_CONFIG_FILE+/data/tier0/admin/ReplayOfflineConfiguration.py+' ./config/tier0/config.py
sed -i 's+TIER0_SPEC_DIR+/data/tier0/admin/Specs+' ./config/tier0/config.py

# Real information for WMStats
sed -i "s+config.Agent.teamName = 'REPLACE_TEAM_NAME'+config.Agent.teamName = 'Tier0Replay'+" ./config/tier0/config.py
sed -i "s+config.Agent.contact = 'cms-comp-ops-workflow-team@cern.ch'+config.Agent.contact = 'cms-tier0-operations@cern.ch'+" ./config/tier0/config.py


#
# Use this team and not the default 
#
#sed -i "s+'team1,team2,cmsdataops'+'tier0production'+g" ./config/tier0/config.py
sed -i "s+'team1,team2,cmsdataops'+'tier0replay'+g" ./config/tier0/config.py

#
# configure retry settings
#
echo "config.RetryManager.PauseAlgo.default.coolOffTime = {'create': 10, 'job': 10, 'submit': 10}" >> ./config/tier0/config.py

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

# Twiking Rucio configuration
sed -i "s+config.RucioInjector.listTiersToInject.*+config.RucioInjector.listTiersToInject = ['AOD', 'MINIAOD', 'NANOAOD', 'NANOAODSIM', 'RAW', 'FEVT', 'USER', 'ALCARECO', 'ALCAPROMPT', 'DQMIO','RAW-RECO']+" ./config/tier0/config.py
sed -i "s+config.RucioInjector.containerDiskRuleParams.*+config.RucioInjector.containerDiskRuleParams = {'lifetime': 7 * 24 * 60 * 60}+" ./config/tier0/config.py
sed -i "s+config.RucioInjector.metaDIDProject.*+config.RucioInjector.metaDIDProject = 'Test'+" ./config/tier0/config.py
echo "config.RucioInjector.blockRuleParams = {'lifetime': 7 * 24 * 60 * 60}" >> ./config/tier0/config.py
echo "config.RucioInjector.blockDeletionDelayHours = 2" >> ./config/tier0/config.py
#
# Set output datasets status to VALID in DBS
#
echo "config.DBS3Upload.datasetType = 'VALID'" >> ./config/tier0/config.py
sed -i "s+config.DBS3Upload.uploaderName = 'WMAgent'+config.DBS3Upload.uploaderName = 'T0Replay'+g" ./config/tier0/config.py

#
# needed for conditions upload
#
echo "config.Tier0Feeder.serviceProxy = '/data/certs/robot-proxy-vocms001.pem'" >> ./config/tier0/config.py

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
# upload PromptReco performance data
#
echo 'config.TaskArchiver.dashBoardUrl = "http://dashb-luminosity.cern.ch/dashboard/request.py/putluminositydata"' >> ./config/tier0/config.py
echo 'config.TaskArchiver.logLevel = "DEBUG"' >> ./config/tier0/config.py

#
# Workflow archive delay
#
#echo 'config.TaskArchiver.archiveDelayHours = 1' >> ./config/tier0/config.py

#
# Do not use WorkQueue
#
echo 'config.TaskArchiver.useWorkQueue = False' >> ./config/tier0/config.py

#
# Enable AgentStatusWatcher - site status automatic updated
#
sed -i "s+config.AgentStatusWatcher.ignoreDisks.*+config.AgentStatusWatcher.ignoreDisks = [ '/cvmfs/cvmfs-config.cern.ch', '/cvmfs/cms.cern.ch', '/eos/cms', '/cvmfs/cms-ib.cern.ch', '/cvmfs/patatrack.cern.ch' ]+" ./config/tier0/config.py
echo "config.AgentStatusWatcher.enabled = False" >> ./config/tier0/config.py
echo "config.AgentStatusWatcher.onlySSB = False" >> ./config/tier0/config.py

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

#Setting for T0_CH_CERN_Disk
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --cms-name=T2_CH_CERN --pnn=T0_CH_CERN_Disk --ce-name=T2_CH_CERN --pending-slots=20000 --running-slots=20000 --plugin=SimpleCondorPlugin
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T0_CH_CERN_Disk --cms-name=T0_CH_CERN_Disk --pnn=T2_CH_CERN --ce-name=T0_CH_CERN_Disk --pending-slots=20000 --running-slots=20000 --plugin=SimpleCondorPlugin

#Setting for T2_CH_CERN
#./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --cms-name=T2_CH_CERN --pnn=T2_CH_CERN --ce-name=T2_CH_CERN --pending-slots=20000 --running-slots=20000 --plugin=SimpleCondorPlugin

./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Processing --pending-slots=10000 --running-slots=10000
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Merge --pending-slots=1000 --running-slots=1000
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Cleanup --pending-slots=1000 --running-slots=1000
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=LogCollect --pending-slots=1000 --running-slots=1000
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Skim --pending-slots=1 --running-slots=1
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Production --pending-slots=1 --running-slots=1
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Harvesting --pending-slots=1000 --running-slots=1000
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Express --pending-slots=3000 --running-slots=3000
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Repack --pending-slots=5000 --running-slots=5000

#Settings for using T2_CH_CERN_P5 (PromptReco)
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --cms-name=T2_CH_CERN_P5 --pnn=T2_CH_CERN_P5 --ce-name=T2_CH_CERN_P5 --pending-slots=20000 --running-slots=20000 --plugin=SimpleCondorPlugin
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Processing --pending-slots=10000 --running-slots=10000
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Merge --pending-slots=1000 --running-slots=1000
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Cleanup --pending-slots=1000 --running-slots=1000
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=LogCollect --pending-slots=1000 --running-slots=1000
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Skim --pending-slots=1 --running-slots=1
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Production --pending-slots=1 --running-slots=1
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Harvesting --pending-slots=1000 --running-slots=1000

# Thresholds configurations
echo "config.AgentStatusWatcher.t1SitesCores = 12.5"  >> ./config/tier0/config.py

echo "config.AgentStatusWatcher.pendingSlotsTaskPercent = 30" >> ./config/tier0/config.py
echo "config.AgentStatusWatcher.pendingSlotsSitePercent = 40" >> ./config/tier0/config.py

echo "config.AgentStatusWatcher.runningExpressPercent = 25" >> ./config/tier0/config.py
echo "config.AgentStatusWatcher.runningRepackPercent = 10" >> ./config/tier0/config.py

#Configurable retry number for failing jobs before they go to paused
echo "config.RetryManager.PauseAlgo.section_('Express')" >> ./config/tier0/config.py
echo "config.RetryManager.PauseAlgo.Express.retryErrorCodes = { 70: 0, 50660: 0, 50661: 0, 50664: 0, 71304: 0 }" >> ./config/tier0/config.py
echo "config.RetryManager.PauseAlgo.section_('Processing')" >> ./config/tier0/config.py
echo "config.RetryManager.PauseAlgo.Processing.retryErrorCodes = { 70: 0, 50660: 0, 50661: 1, 50664: 0, 71304: 1 }" >> ./config/tier0/config.py
echo "config.RetryManager.PauseAlgo.section_('Repack')" >> ./config/tier0/config.py
echo "config.RetryManager.PauseAlgo.Repack.retryErrorCodes = { 70: 0, 50660: 0, 50661: 0, 50664: 0, 71304: 0 }" >> ./config/tier0/config.py

#Overwrite RetryManager to show Logcollect and CleanUp jobs paused instead of automatically fails
sed -i "s/config.RetryManager.plugins.*/config.RetryManager.plugins={'default': 'PauseAlgo', 'Cleanup': 'PauseAlgo', 'LogCollect': 'PauseAlgo'}/g" ./config/tier0/config.py

#Overwrite ErrorHandler to ensure T0 jobs can always be retried
sed -i "s/config.ErrorHandler.maxFailTime.*/config.ErrorHandler.maxFailTime=601200/g" ./config/tier0/config.py
sed -i "s/config.ErrorHandler.maxRetries.*/config.ErrorHandler.maxRetries={'default': 30, 'Cleanup': 30, 'LogCollect': 30}/g" ./config/tier0/config.py
