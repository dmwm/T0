#!/bin/bash 

DEPLOY_DIR=/data/tier0/WMAgent.venv3
cd $DEPLOY_DIR
echo "Activating WMAgent virtual environment"
sleep 3
source $DEPLOY_DIR/bin/activate

echo "Cleaning T0AST database"
sleep 3
#We use old script meanwhile issue with clean-oracle command is solved
bash /data/tier0/00_wipe_t0ast.sh
#manage clean-oracle

echo "Now initializing"
sleep 3
bash $DEPLOY_DIR/init.sh

echo "Now populating resource control"


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
sed -i 's+TIER0_CONFIG_FILE+/data/tier0/admin/ProdOfflineConfiguration.py+' $config/config.py
sed -i 's+TIER0_SPEC_DIR+/data/tier0/admin/Specs+' $config/config.py
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

