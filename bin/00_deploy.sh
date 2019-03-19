#!/bin/bash

BASE_DIR=/data/tier0
DEPLOY_DIR=$BASE_DIR/srv/wmagent
SPEC_DIR=$BASE_DIR/admin/Specs

TIER0_VERSION=1.9.94
TIER0_ARCH=slc6_amd64_gcc481

rm -rf $DEPLOY_DIR
mkdir -p $DEPLOY_DIR

rm -rf $SPEC_DIR
mkdir -p $SPEC_DIR

cd $BASE_DIR
rm -rf deployment
git clone https://github.com/dmwm/deployment.git
cd deployment
git pull --no-edit https://github.com/hufnagel/deployment tier0-remove-k5reauth
git pull --no-edit https://github.com/ticoann/deployment tier0_couch16

# install from hufnagel private repo
sed -i 's+comp.pre+comp.pre.hufnagel+' tier0/deploy

# override tier0 deployment code
#rm -rf tier0
#cp -a /data/tier0/deployment_tier0 tier0

echo ""
echo " *** Deploying Tier0 WMAgent *** "
./Deploy -s prep -A $TIER0_ARCH -t $TIER0_VERSION -R tier0@$TIER0_VERSION $DEPLOY_DIR tier0@$TIER0_VERSION
./Deploy -s sw -A $TIER0_ARCH -t $TIER0_VERSION -R tier0@$TIER0_VERSION $DEPLOY_DIR tier0@$TIER0_VERSION
./Deploy -s post -A $TIER0_ARCH -t $TIER0_VERSION -R tier0@$TIER0_VERSION $DEPLOY_DIR tier0@$TIER0_VERSION

## global patch override
echo ""
echo " *** Applying general patches and cleaning t0ast *** "
$BASE_DIR/00_patches.sh 2>&1 > /dev/null

## clean database
$BASE_DIR/00_wipe_t0ast.sh 2>&1 > /dev/null

# needs secret file location and user certs
source $BASE_DIR/admin/env.sh

cd $DEPLOY_DIR/current

echo ""
echo " *** Initializing services / agent *** "
./config/tier0/manage activate-tier0
./config/tier0/manage start-services
./config/tier0/manage init-tier0
sleep 5

#
# mandatory configuration tweaks
#
sed -i 's+TIER0_CONFIG_FILE+/data/tier0/admin/ReplayOfflineConfiguration.py+' ./config/tier0/config.py
sed -i 's+TIER0_SPEC_DIR+/data/tier0/admin/Specs+' ./config/tier0/config.py
sed -i "s+OP EMAIL+luis89@fnal.gov+g" ./config/tier0/config.py
sed -i "s+'wmagentalerts@gmail.com'+'luis89@fnal.gov','john.casallas@cern.ch'+g" ./config/tier0/config.py
#sed -i "s+OP EMAIL+Dirk.Hufnagel@cern.ch+g" ./config/tier0/config.py
#sed -i "s+wmagentalerts@gmail.com+Dirk.Hufnagel@cern.ch+g" ./config/tier0/config.py

#
# configure Condor settings
#
echo "config.BossAir.pluginNames = ['CondorPlugin']" >> ./config/tier0/config.py

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
sed -i "s+config.PhEDExInjector.logLevel = 'INFO'+config.PhEDExInjector.logLevel = 'DEBUG'+g" ./config/tier0/config.py
sed -i "s+config.DBS3Upload.logLevel = 'INFO'+config.DBS3Upload.logLevel = 'DEBUG'+g" ./config/tier0/config.py
#sed -i "s+config.JobCreator.logLevel = 'INFO'+config.JobCreator.logLevel = 'DEBUG'+g" ./config/tier0/config.py

#
# configure shorter polling cyles
#
#echo 'config.ErrorHandler.pollInterval = 30' >> ./config/tier0/config.py
#echo 'config.RetryManager.pollInterval = 30' >> ./config/tier0/config.py
#echo 'config.DBS3Upload.pollInterval = 30' >> ./config/tier0/config.py
#echo 'config.PhEDExInjector.pollInterval = 30' >> ./config/tier0/config.py

#
# configure VALID status for datasets
#
#echo 'config.DBS3Upload.datasetType = "VALID"' >> ./config/tier0/config.py

#
# configure Tier0-Mode for PhEDEx
#
#echo 'config.PhEDExInjector.tier0Mode = False' >> ./config/tier0/config.py
#echo 'config.PhEDExInjector.autoDelete = False' >> ./config/tier0/config.py
sed -i "s+config.PhEDExInjector.subscribeInterval = 43200+config.PhEDExInjector.subscribeInterval = 30+g" ./config/tier0/config.py

#
# disable AgentStatusWatcher
#
echo 'config.AgentStatusWatcher.enabled = False' >> ./config/tier0/config.py

#
# needed for LSF DQM uploads
#
#echo 'config.Tier0Feeder.dqmUploadProxy = "/afs/cern.ch/user/h/hufnagel/private/Certificates/dqmcert.pem"' >> ./config/tier0/config.py

#
# needed for conditions upload
#
echo "config.Tier0Feeder.serviceProxy = '/data/certs/serviceproxy-vocms15.pem'" >> ./config/tier0/config.py

#
# password for dropbox upload
#
#echo 'config.Tier0Feeder.dropboxuser = "cmsprod"' >> ./config/tier0/config.py
#echo 'config.Tier0Feeder.dropboxpass = "*******"' >> ./config/tier0/config.py

#
# needed for passing notifications back to StorageManager
#
#echo 'config.Tier0Feeder.transferSystemBaseDir = "/data/tier0/replayinject"' >> ./config/tier0/config.py

#
# upload PromptReco performance data
#
echo 'config.TaskArchiver.dashBoardUrl = "http://dashb-luminosity.cern.ch/dashboard/request.py/putluminositydata"' >> ./config/tier0/config.py
echo 'config.TaskArchiver.logLevel = "DEBUG"' >> ./config/tier0/config.py

#
# Workflow archive delay
#
echo 'config.TaskArchiver.archiveDelayHours = 1' >> ./config/tier0/config.py

#
# Setting up sites
#

./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --cms-name=T2_CH_CERN --se-name=srm-eoscms.cern.ch --ce-name=T2_CH_CERN --pending-slots=0 --running-slots=0 --plugin=CondorPlugin
#./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Processing --pending-slots=0 --running-slots=10000
#./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Merge --pending-slots=0 --running-slots=10000
#./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Cleanup --pending-slots=0 --running-slots=10000
#./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=LogCollect --pending-slots=0 --running-slots=10000
#./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Skim --pending-slots=0 --running-slots=10000
#./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Production --pending-slots=0 --running-slots=10000
#./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Harvesting --pending-slots=0 --running-slots=10000
#./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Express --pending-slots=0 --running-slots=10000
#./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Repack --pending-slots=0 --running-slots=10000
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --down

./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_T0 --cms-name=T2_CH_CERN_T0 --se-name=srm-eoscms.cern.ch --ce-name=T2_CH_CERN_T0 --pending-slots=1200 --running-slots=6000 --plugin=CondorPlugin
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_T0 --task-type=Processing --pending-slots=1200 --running-slots=6000
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_T0 --task-type=Merge --pending-slots=250 --running-slots=250
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_T0 --task-type=Cleanup --pending-slots=250 --running-slots=250
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_T0 --task-type=LogCollect --pending-slots=100 --running-slots=200
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_T0 --task-type=Skim --pending-slots=10 --running-slots=10
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_T0 --task-type=Production --pending-slots=10 --running-slots=10
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_T0 --task-type=Harvesting --pending-slots=50 --running-slots=100
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_T0 --task-type=Express --pending-slots=500 --running-slots=1500
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_T0 --task-type=Repack --pending-slots=250 --running-slots=500
#./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_T0 --down

./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_AI --cms-name=T2_CH_CERN_AI --se-name=eoscmsftp.cern.ch --ce-name=T2_CH_CERN_AI --pending-slots=120 --running-slots=600 --plugin=CondorPlugin
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_AI --task-type=Processing --pending-slots=120 --running-slots=600
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_AI --task-type=Merge --pending-slots=25 --running-slots=25
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_AI --task-type=Cleanup --pending-slots=25 --running-slots=25
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_AI --task-type=LogCollect --pending-slots=10 --running-slots=20
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_AI --task-type=Skim --pending-slots=1 --running-slots=1
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_AI --task-type=Production --pending-slots=1 --running-slots=1
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_AI --task-type=Harvesting --pending-slots=5 --running-slots=10
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_AI --task-type=Express --pending-slots=50 --running-slots=150
./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_AI --task-type=Repack --pending-slots=25 --running-slots=50
#./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_AI --down

#
# set resource thresholds
#
#./config/tier0/manage execute-agent wmagent-resource-control --add-T0 --pending-slots=0 --running-slots=0
#./config/tier0/manage execute-agent wmagent-resource-control --add-T1s --pending-slots=0 --running-slots=0

#./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --cms-name=T2_CH_CERN --se-name=srm-eoscms.cern.ch --ce-name=T2_CH_CERN --pending-slots=100 --running-slots=1000 --plugin=PyCondorPlugin
#./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_T0 --cms-name=T2_CH_CERN_T0 --se-name=srm-eoscms.cern.ch --ce-name=T2_CH_CERN_T0 --pending-slots=1000 --running-slots=3000 --plugin=PyCondorPlugin
#./config/tier0/manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_HLT --cms-name=T2_CH_CERN_HLT --se-name=srm-eoscms.cern.ch --ce-name=T2_CH_CERN_HLT --pending-slots=100 --running-slots=1000 --plugin=PyCondorPlugin
#./config/tier0/manage execute-agent wmagent-resource-control --site-name=T1_US_FNAL_Disk --cms-name=T1_US_FNAL_Disk --se-name=cmssrmdisk.fnal.gov --ce-name=T1_US_FNAL --pending-slots=100 --running-slots=1000 --plugin=PyCondorPlugin

# Use this sites:
#echo "config.AgentStatusWatcher.forcedSiteList = [ 'T2_CH_CERN_T0' ]" >> ./config/tier0/config.py

# Thresholds configurations
#echo "config.AgentStatusWatcher.pendingSlotsTaskPercent = 30" >> ./config/tier0/config.py
#echo "config.AgentStatusWatcher.pendingSlotsSitePercent = 30" >> ./config/tier0/config.py

#echo "config.AgentStatusWatcher.runningExpressPercent = 30" >> ./config/tier0/config.py
#echo "config.AgentStatusWatcher.runningRepackPercent = 10" >> ./config/tier0/config.py


