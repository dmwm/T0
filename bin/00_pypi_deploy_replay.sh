#!/bin/bash 

confirm_clearing=""
echo "This will clear the oracle database, couchdb, and important agent directories"
sleep 5
echo "Are you sure you wish to continue? (Y/n)"
read confirm_clearing

if [ "$confirm_clearing" != "Y" ]
then
    echo "Not performing changes"
    sleep 2
    echo "Exiting"
    exit
fi

WMAGENT_TAG=2.3.4rc11
TIER0_VERSION=3.2.2
COUCH_TAG=3.2.2

BASE_DIR=/data/tier0
DEPLOY_DIR=$BASE_DIR/WMAgent.venv3
SPEC_DIR=$BASE_DIR/admin/Specs
CURRENT_DIR=$DEPLOY_DIR/srv/wmagent/$WMAGENT_TAG

CONFIGURATION_FILE='/data/tier0/admin/ReplayOfflineConfiguration.py'
WMAGENT_SECRETS=$BASE_DIR/admin/WMAgent.secrets.replay
CERT=/data/certs/robot-cert-cmst0.pem
KEY=/data/certs/robot-key-cmst0.pem
PROXY=/data/certs/robot-proxy-vocms001.pem

WMA_VENV_DEPLOY_SCRIPT=https://raw.githubusercontent.com/dmwm/WMCore/$WMAGENT_TAG/deploy/deploy-wmagent-venv.sh
echo "Resetting couchdb for new deployment"
sleep 3
bash $BASE_DIR/00_pypi_reset_couch.sh -t $COUCH_TAG

cd $BASE_DIR

echo "Removing deploy directory"
sleep 3
rm -rf $DEPLOY_DIR

echo "Clearing Specs directory"
sleep 3
rm -rf $SPEC_DIR/*

echo "Clearing Oracle Database"
sleep 3
bash $BASE_DIR/00_wipe_t0ast.sh

echo "Installing new wmagent"
echo "WMAgent version $WMAGENT_TAG"
sleep 3

rm $BASE_DIR/deploy-wmagent-venv.sh
wget $WMA_VENV_DEPLOY_SCRIPT -O $BASE_DIR/deploy-wmagent-venv.sh
sed -i 's|\$WMA_CERTS_DIR/myproxy.pem|\$WMA_CERTS_DIR/robot-proxy-vocms001.pem|g' $BASE_DIR/deploy-wmagent-venv.sh
#bash $BASE_DIR/deploy-wmagent-venv.sh -t $WMAGENT_TAG -d $DEPLOY_DIR -y -s

bash $BASE_DIR/deploy-wmagent-venv.sh -t $WMAGENT_TAG -d $DEPLOY_DIR -y

#######################################################################
echo "Setting up secrets file"
sleep 1
ln -s $WMAGENT_SECRETS $DEPLOY_DIR/admin/wmagent/WMAgent.secrets

echo "Setting up certificate and key"
sleep 1
rm $DEPLOY_DIR/certs/*
ln -s $CERT $DEPLOY_DIR/certs/servicecert.pem
ln -s $KEY $DEPLOY_DIR/certs/servicekey.pem
ln -s $PROXY $DEPLOY_DIR/certs/myproxy.pem
#######################################################################

echo "Activating environment"
sleep 2
cd $DEPLOY_DIR
source $DEPLOY_DIR/bin/activate
echo "Installing T0 code"
sleep 3
pip install T0==$TIER0_VERSION

chmod +x $DEPLOY_DIR/bin/00*
chmod +x $DEPLOY_DIR/bin/t0

echo "Applying patches"
bash $BASE_DIR/00_pypi_patches.sh


echo "Now creating important T0 related environment variables"
sleep 2
echo "WMCORE_CACHE_DIR=/tmp/cmst0"
echo "install=$CURRENT_DIR/install"
echo "config=$CURRENT_DIR/config"
echo "manage=manage"
sleep 1
### The WMCoreVenvVars is a function in the $DEPLOY_DIR/bin/activate file
declare -A WMCoreVenvVars
WMCoreVenvVars[WMCORE_CACHE_DIR]=/tmp/$(whoami)
WMCoreVenvVars[install]=$CURRENT_DIR/install
WMCoreVenvVars[config]=$CURRENT_DIR/config
WMCoreVenvVars[manage]=manage
_WMCoreVenvSet ${!WMCoreVenvVars[@]}
sleep 1
echo "variables created successfully"
sleep 1

###########################

echo "Now initializing"
sleep 3
bash $DEPLOY_DIR/init.sh

echo "Now populating resource control"
sleep 3
bash $DEPLOY_DIR/bin/00_pypi_resource_control.sh

echo "Modifying config file"
sleep 3
#####
sed -i 's+TIER0_CONFIG_FILE+'"$CONFIGURATION_FILE"'+' "$config/config.py"
#####
sed -i "s+config.Agent.teamName = 'REPLACE_TEAM_NAME'+config.Agent.teamName = '"$TEAMNAME"'+" "$config/config.py"
#####
sed -i "s+config.Agent.contact = 'cms-comp-ops-workflow-team@cern.ch'+config.Agent.contact = 'cms-tier0-operations@cern.ch'+" "$config/config.py"
#####
sed -i "s+'team1,team2,cmsdataops'+'tier0replay'+g" "$config/config.py"
#####
sed -i "s+config.RucioInjector.containerDiskRuleParams.*+config.RucioInjector.containerDiskRuleParams = {'lifetime': 7 * 24 * 60 * 60}+" "$config/config.py"
#####
echo "config.RucioInjector.blockRuleParams = {'lifetime': 7 * 24 * 60 * 60}" >> "$config/config.py"
#####
sed -i "s+config.RucioInjector.metaDIDProject.*+config.RucioInjector.metaDIDProject = 'Test'+" "$config/config.py"
#####
echo "config.RucioInjector.blockDeletionDelayHours = 2" >> $config/config.py
#####
##### ONLY IN PROD #####
#echo "config.RucioInjector.blockDeletionDelayHours = 168" >> ./config/tier0/config.py
#echo 'config.BossAir.pluginNames = ["SimpleCondorPlugin"]' >> ./config/tier0/config.py
#echo 'config.JobAccountant.maxAllowedRepackOutputSize = 24 * 1024 * 1024 * 1024' >> ./config/tier0/config.py
#echo "config.AgentStatusWatcher.runningExpressPercent = 25" >> ./config/tier0/config.py
#echo "config.AgentStatusWatcher.runningRepackPercent = 10" >> ./config/tier0/config.py
#echo 'config.TaskArchiver.archiveDelayHours = 2190' >> $config.py
##### ONLY IN PROD #####
#####
echo "config.DBS3Upload.datasetType = 'VALID'" >> $config/config.py
#####
echo "config.Tier0Feeder.serviceProxy = '$DEPLOY_DIR/certs/myproxy.pem'" >> $config/config.py
#####
echo 'config.TaskArchiver.dashBoardUrl = "http://dashb-luminosity.cern.ch/dashboard/request.py/putluminositydata"' >> $config/config.py
#####
sed -i "s+config.DBS3Upload.uploaderName = 'WMAgent'+config.DBS3Upload.uploaderName = 'T0Replay'+g" "$config/config.py"
#####
#Overwrite ErrorHandler to avoid jobs going to ensure T0 jobs can always be retried
sed -i "s/config.ErrorHandler.maxFailTime.*/config.ErrorHandler.maxFailTime=601200/g" "$config/config.py"
#####
sed -i "s+config.RucioInjector.listTiersToInject.*+config.RucioInjector.listTiersToInject = ['AOD', 'MINIAOD', 'NANOAOD', 'NANOAODSIM', 'RAW', 'FEVT', 'USER', 'ALCARECO', 'ALCAPROMPT','DQMIO','RAW-RECO']+" "$config/config.py"
#####
##### ONLY IN REPLAY #####
sed -i "s/config.RetryManager.plugins.*/config.RetryManager.plugins={'default': 'PauseAlgo', 'Cleanup': 'PauseAlgo', 'LogCollect': 'PauseAlgo'}/g" "$config/config.py"
sed -i "s/config.ErrorHandler.maxRetries.*/config.ErrorHandler.maxRetries={'default': 30, 'Cleanup': 30, 'LogCollect': 30}/g" "$config/config.py"
##### ONLY IN REPLAY #####

#
# Enable AgentStatusWatcher - site status automatic updated
#
sed -i "s+config.AgentStatusWatcher.ignoreDisks.*+config.AgentStatusWatcher.ignoreDisks = [ '/cvmfs/cvmfs-config.cern.ch', '/cvmfs/cms.cern.ch', '/eos/cms', '/cvmfs/cms-ib.cern.ch', '/cvmfs/patatrack.cern.ch' ]+" "$config/config.py"


#
# password for dropbox upload
#

DROPBOX_USER=`cat $WMA_SECRETS_FILE | grep DROPBOX_USER | sed s/DROPBOX_USER=//`
DROPBOX_PASS=`cat $WMA_SECRETS_FILE | grep DROPBOX_PASS | sed s/DROPBOX_PASS=//`

if [ "x$DROPBOX_USER" == "x" ] || [ "x$DROPBOX_PASS" == "x" ]; then
    echo "Secrets file doesn't contain DROPBOX_USER or DROPBOX_PASS";
    exit 1
fi

echo 'config.Tier0Feeder.dropboxuser = "'$DROPBOX_USER'"' >> $config/config.py
echo 'config.Tier0Feeder.dropboxpass = "'$DROPBOX_PASS'"' >> $config/config.py


sleep 1
echo "You are now in the WMAgent environment"

sleep 1
echo "Deployment finished"

cd $BASE_DIR

