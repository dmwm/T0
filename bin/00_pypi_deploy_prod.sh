#!/bin/bash 

confirm_clearing=""

echo "You are about to deploy production. Please name the node you intend to deploy (include .cern.ch : vocms001.cern.ch)"
read HOST

echo -e "\n"
if [ "$HOST" != "$(hostname)" ] 
then
    sleep 1
    echo "Your answer was $HOST"
    sleep 1
    echo "Your current host is $(hostname)"
    sleep 1
    echo "Please ensure you are in the node you want to deploy. Exiting without making changes"
    exit
fi

echo "This will clear the oracle database, couchdb, and important agent directories assosiated to $(hostname)"
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

WMAGENT_TAG=2.4.2
TIER0_VERSION=3.5.1
COUCH_TAG=3.2.2

BASE_DIR=/data/tier0
DEPLOY_DIR=$BASE_DIR/WMAgent.venv3
SPEC_DIR=$BASE_DIR/admin/Specs
CURRENT_DIR=$DEPLOY_DIR/srv/wmagent/$WMAGENT_TAG

CONFIGURATION_FILE='/data/tier0/admin/ProdOfflineConfiguration.py'
WMAGENT_SECRETS=$BASE_DIR/admin/WMAgent.secrets.prod
CERT=/data/certs/robot-cert-cmst0.pem
KEY=/data/certs/robot-key-cmst0.pem
PROXY=/data/certs/robot-proxy-vocms001.pem
RUCIO_CONFIG=$DEPLOY_DIR/etc/rucio.cfg
RUCIO_HOST=$(grep '^RUCIO_HOST=' $WMAGENT_SECRETS | cut -d'=' -f2)
RUCIO_AUTH=$(grep '^RUCIO_AUTH=' $WMAGENT_SECRETS | cut -d'=' -f2)
RUCIO_ACCOUNT=$(grep '^RUCIO_ACCOUNT=' $WMAGENT_SECRETS | cut -d'=' -f2)
WMA_VENV_DEPLOY_SCRIPT=https://raw.githubusercontent.com/dmwm/WMCore/$WMAGENT_TAG/deploy/deploy-wmagent-venv.sh

echo "Resetting couchdb for new deployment"
rm -rf /data/dockerMount/srv/couchdb/*
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

#bash $BASE_DIR/deploy-wmagent-venv.sh -t $WMAGENT_TAG -d $DEPLOY_DIR -y
bash $BASE_DIR/deploy-wmagent-venv.sh -t $WMAGENT_TAG -d $DEPLOY_DIR -p /usr/bin/python3.12 -y
#######################################################################
echo "Setting up secrets file"
sleep 1
ln -s $WMAGENT_SECRETS $DEPLOY_DIR/admin/wmagent/WMAgent.secrets

echo "Setting up certificate and key"
sleep 1
rm $DEPLOY_DIR/certs/*
ln -s $CERT $DEPLOY_DIR/certs/servicecert.pem
ln -s $KEY $DEPLOY_DIR/certs/servicekey.pem
 
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
chmod +x $DEPLOY_DIR/etc/t0

echo "Applying patches"
bash $BASE_DIR/00_pypi_patches.sh


echo "Now creating important T0 related environment variables"
sleep 2
echo "WMCORE_CACHE_DIR=/tmp/cmst0"
echo "install=$CURRENT_DIR/install"
echo "config=$CURRENT_DIR/config"
echo "manage=manage"
sleep 1


echo "Now initializing"
sleep 2
bash $DEPLOY_DIR/init.sh

echo "Fixing proxy"
sleep 1

rm $DEPLOY_DIR/certs/myproxy.pem
ln -s $PROXY $DEPLOY_DIR/certs/robot-proxy-vocms001.pem
ln -s $PROXY $DEPLOY_DIR/certs/myproxy.pem

echo "Adding useful environment variables"
sleep 1
source $DEPLOY_DIR/bin/manage-common.sh
_load_wmasecrets
### The WMCoreVenvVars is a function in the $DEPLOY_DIR/bin/activate file
declare -A WMCoreVenvVars
WMCoreVenvVars[TEAM]=$TEAMNAME
WMCoreVenvVars[WMCORE_CACHE_DIR]=/tmp/$(whoami)
WMCoreVenvVars[install]=$CURRENT_DIR/install
WMCoreVenvVars[config]=$CURRENT_DIR/config
WMCoreVenvVars[manage]=manage
_WMCoreVenvSet ${!WMCoreVenvVars[@]}

sleep 1
echo "variables created successfully"
sleep 1

echo "Now populating resource control"
sleep 2
bash $BASE_DIR/00_pypi_resource_control.sh

echo "Modifying config file"
sleep 3
#####
sed -i 's+TIER0_CONFIG_FILE+'"$CONFIGURATION_FILE"'+' "$config/config.py"
#####
sed -i "s+config.Agent.teamName = 'REPLACE_TEAM_NAME'+config.Agent.teamName = '"$TEAMNAME"'+" "$config/config.py"
#####
sed -i "s+config.Agent.contact = 'cms-comp-ops-workflow-team@cern.ch'+config.Agent.contact = 'cms-tier0-operations@cern.ch'+" "$config/config.py"
#####
sed -i "s+'team1,team2,cmsdataops'+'tier0production'+g" "$config/config.py"
#####
sed -i "s+config.RucioInjector.containerDiskRuleParams.*+config.RucioInjector.containerDiskRuleParams = {}+" "$config/config.py"
#####
echo "config.RucioInjector.blockRuleParams = {}" >> $config/config.py
#####
sed -i "s+config.RucioInjector.metaDIDProject.*+config.RucioInjector.metaDIDProject = 'Tier0'+" "$config/config.py"
#####
echo "config.RucioInjector.blockDeletionDelayHours = 168" >> $config/config.py
#####
##### NOT IN REPLAY #####
echo 'config.BossAir.pluginNames = ["SimpleCondorPlugin"]' >> $config/config.py
echo 'config.JobAccountant.maxAllowedRepackOutputSize = 24 * 1024 * 1024 * 1024' >> $config/config.py
echo "config.AgentStatusWatcher.runningExpressPercent = 25" >> $config/config.py
echo "config.AgentStatusWatcher.runningRepackPercent = 10" >> $config/config.py
echo 'config.TaskArchiver.archiveDelayHours = 720' >> $config.py
##### NOT IN REPLAY #####
#####
echo "config.DBS3Upload.datasetType = 'VALID'" >> $config/config.py
#####
echo "config.Tier0Feeder.serviceProxy = '$DEPLOY_DIR/certs/myproxy.pem'" >> $config/config.py
#####
echo 'config.TaskArchiver.dashBoardUrl = "http://dashb-luminosity.cern.ch/dashboard/request.py/putluminositydata"' >> $config/config.py
#####
sed -i "s+config.DBS3Upload.uploaderName = 'WMAgent'+config.DBS3Upload.uploaderName = 'T0Prod'+g" "$config/config.py"
#####
sed -i "s/config.ErrorHandler.maxFailTime.*/config.ErrorHandler.maxFailTime=601200/g" "$config/config.py"
#####


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
echo "Modifying rucio.cfg"
sleep 1

sed -i "s+rucio_host = RUCIO_HOST_OVERWRITE+rucio_host = ${RUCIO_HOST}+" "$RUCIO_CONFIG"
sed -i "s+auth_host = RUCIO_AUTH_OVERWRITE+auth_host = ${RUCIO_AUTH}+" "$RUCIO_CONFIG"
echo -e "\n" >> $RUCIO_CONFIG
echo "account = $RUCIO_ACCOUNT" >> "$RUCIO_CONFIG"

sleep 1
echo "You are now in the WMAgent environment"

sleep 1


cd $BASE_DIR

