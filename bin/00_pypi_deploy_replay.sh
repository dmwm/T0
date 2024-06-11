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

WMAGENT_TAG=2.3.4rc4
TIER0_VERSION=3.2.0
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

echo "Resetting couchdb for new deployment"
sleep 3
bash $BASE_DIR/00_reset_couch.sh -t $COUCH_TAG

cd $BASE_DIR

echo "Removing deploy directory"
sleep 3
rm -rfv $DEPLOY_DIR

echo "Clearing Specs directory"
sleep 3
rm -rfv $SPEC_DIR/*

echo "Clearing Oracle Database"
sleep 3
bash $BASE_DIR/00_wipe_t0ast.sh

echo "Installing new wmagent"
echo "WMAgent version $WMAGENT_TAG"
sleep 3

bash $BASE_DIR/deploy-wmagent-venv.sh -t $WMAGENT_TAG -d $DEPLOY_DIR -y -s

#######################################################################
echo "Setting up secrets file"
sleep 1
ln -s $WMAGENT_SECRETS $DEPLOY_DIR/admin/wmagent/WMAgent.secrets

echo "Setting up certificate and key"
sleep 1
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

#export install=$CURRENT_DIR/install
#export config=$CURRENT_DIR/config
#export manage=manage

#echo "activating additional environment variables"
#source $WMA_ENV_FILE

cp $BASE_DIR/Tier0Config.py $DEPLOY_DIR/etc/Tier0Config.py

###########################

echo "Now initializing"
sleep 3
bash $DEPLOY_DIR/init.sh

echo "Now populating resource control"
sleep 3

#Setting for T0_CH_CERN_Disk
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --cms-name=T2_CH_CERN --pnn=T0_CH_CERN_Disk --ce-name=T2_CH_CERN --pending-slots=20000 --running-slots=20000 --plugin=SimpleCondorPlugin
manage execute-agent wmagent-resource-control --site-name=T0_CH_CERN_Disk --cms-name=T0_CH_CERN_Disk --pnn=T2_CH_CERN --ce-name=T0_CH_CERN_Disk --pending-slots=20000 --running-slots=20000 --plugin=SimpleCondorPlugin

#Setting for T2_CH_CERN
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --cms-name=T2_CH_CERN --pnn=T2_CH_CERN --ce-name=T2_CH_CERN --pending-slots=20000 --running-slots=20000 --plugin=SimpleCondorPlugin

manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Processing --pending-slots=10000 --running-slots=10000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Merge --pending-slots=1000 --running-slots=1000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Cleanup --pending-slots=1000 --running-slots=1000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=LogCollect --pending-slots=1000 --running-slots=1000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Skim --pending-slots=1 --running-slots=1
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Production --pending-slots=1 --running-slots=1
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Harvesting --pending-slots=1000 --running-slots=1000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Express --pending-slots=3000 --running-slots=3000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Repack --pending-slots=5000 --running-slots=5000

#Settings for using T2_CH_CERN_P5 (PromptReco)
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --cms-name=T2_CH_CERN_P5 --pnn=T2_CH_CERN_P5 --ce-name=T2_CH_CERN_P5 --pending-slots=20000 --running-slots=20000 --plugin=SimpleCondorPlugin
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Processing --pending-slots=10000 --running-slots=10000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Merge --pending-slots=1000 --running-slots=1000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Cleanup --pending-slots=1000 --running-slots=1000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=LogCollect --pending-slots=1000 --running-slots=1000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Skim --pending-slots=1 --running-slots=1
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Production --pending-slots=1 --running-slots=1
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Harvesting --pending-slots=1000 --running-slots=1000

echo "Modifying config file"
sleep 3
sed -i 's+TIER0_CONFIG_FILE+'"$CONFIGURATION_FILE"'+' "$config/config.py"

sed -i "s+config.Agent.contact = 'cms-comp-ops-workflow-team@cern.ch'+config.Agent.contact = 'cms-tier0-operations@cern.ch'+" $config/config.py
sed -i "s+'team1,team2,cmsdataops'+'tier0production'+g" $config/config.py


# Twiking Rucio configuration
sed -i "s+config.RucioInjector.containerDiskRuleParams.*+config.RucioInjector.containerDiskRuleParams = {}+" $config/config.py
sed -i "s+config.RucioInjector.metaDIDProject.*+config.RucioInjector.metaDIDProject = 'Tier0'+" $config/config.py

sed -i "s+config.DBS3Upload.uploaderName = 'WMAgent'+config.DBS3Upload.uploaderName = 'T0Prod'+g" $config/config.py

#
# Enable AgentStatusWatcher - site status automatic updated
#
sed -i "s+config.AgentStatusWatcher.ignoreDisks.*+config.AgentStatusWatcher.ignoreDisks = [ '/cvmfs/cvmfs-config.cern.ch', '/cvmfs/cms.cern.ch', '/eos/cms', '/cvmfs/cms-ib.cern.ch', '/cvmfs/patatrack.cern.ch' ]+" $config/config.py


#Overwrite ErrorHandler to avoid jobs going to ensure T0 jobs can always be retried
sed -i "s/config.ErrorHandler.maxFailTime.*/config.ErrorHandler.maxFailTime=601200/g" $config/config.py

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
