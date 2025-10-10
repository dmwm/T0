#!/bin/bash 

BASE_DIR=/data/tier0
DEPLOY_DIR=$BASE_DIR/WMAgent.venv3
CURRENT_DIR=$DEPLOY_DIR/srv/wmagent/current
SPEC_DIR=$BASE_DIR/admin/Specs

COUCH_DIR=/data/CMSKubernetes/docker/pypi/wmagent-couchdb
COUCH_TAG=3.2.2

RUCIO_CONFIG=$DEPLOY_DIR/etc/rucio.cfg
RUCIO_HOST=$(grep '^RUCIO_HOST=' $WMA_SECRETS_FILE | cut -d'=' -f2)
RUCIO_AUTH=$(grep '^RUCIO_AUTH=' $WMA_SECRETS_FILE | cut -d'=' -f2)
RUCIO_ACCOUNT=$(grep '^RUCIO_ACCOUNT=' $WMA_SECRETS_FILE | cut -d'=' -f2)

CLEAR=0
while getopts "RPh" opt; do
    case $opt in
        R)
            if [ "$CLEAR" -eq 0 ]
            then
                clear-replay
                replay-secrets
                init
                tweak-replay-config
                configure-dropbox
                configure-rucio
                resource-control
                CLEAR=1
            else
                help-message
            fi
            ;;
        P)
            if [ "$CLEAR" -eq 0 ]
            then
                clear-production
                production-secrets
                init
                tweak-prod-config
                configure-dropbox
                configure-rucio
                resource-control
                CLEAR=1
            else
                help-message
            fi
            ;;
        h)
            help-message ;;

    esac
done

shift $((OPTIND - 1))  # Now $1 is first non-option argument, $2 is second, etc.

if [ -n "$1" ]; then
    t0 --set-agent-name="$1"
else
    t0 --set-agent-name="MainAgent"
fi

function help-message()
{
    echo "To use this script, make sure T0 and wmagent code have been installed."
    echo "To install T0 and wmagent code see install.sh -h"

    echo "-R : deploy replay"
    echo "-P : deploy production"

    echo "Sample usage: source /data/tier0/deploy.sh -R"
}

function clear()
{
    echo " "
    echo "clearing previous deployment. You still have 5 seconds to regret..."
    echo " "

    sleep 4

    echo "Here we go"
    sleep 1

    echo "Clearing Oracle Database"
    sleep 1
    bash $BASE_DIR/00_wipe_t0ast.sh

    echo "Clearing Specs directory"
    sleep 1
    rm -rf $SPEC_DIR/*

    echo "Resetting local couchdb"
    sleep 1
    docker kill couchdb
    rm -rf /data/dockerMount/srv/couchdb/*
    bash $COUCH_DIR/couchdb-docker-run.sh -t $COUCH_TAG -p
}

function clear-production()
{
    echo " "
    echo "Running clear-production"
    echo " "

    sleep 1

    confirm_clearing=""

    echo "You are about to clear a production node."
    echo "Please name the node you intend to clear for a new deployment (include .cern.ch : vocms001.cern.ch)"
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
        sleep 1
        echo "Exiting"
        exit
    else
        echo "Clearing Prod node $current_host"
        clear
    fi

}

function clear-replay()
{
    echo " "
    echo "Running clear-replay"
    echo " "

    sleep 1

    allowed_hosts="vocms047.cern.ch vocms0500.cern.ch vocms05011.cern.ch vocms05012.cern.ch"
    current_host=$(hostname)

    if [[ " $allowed_hosts " =~ " $current_host " ]]; then
        echo "Clearing Replay node $current_host"
        sleep 1
        clear
    else
        clear-production
    fi

}

function replay-secrets()
{
    echo " "
    echo "Running replay-secrets"
    echo " "

    sleep 1

    rm $BASE_DIR/admin/WMAgent.secrets
    ln -s $BASE_DIR/admin/WMAgent.secrets.replay $BASE_DIR/admin/WMAgent.secrets
    ln -s $BASE_DIR/admin/WMAgent.secrets.replay $DEPLOY_DIR/admin/wmagent/WMAgent.secrets
}

function production-secrets()
{
    echo " "
    echo "Running production-secrets"
    echo " "

    sleep 1

    rm $BASE_DIR/admin/WMAgent.secrets
    ln -s $BASE_DIR/admin/WMAgent.secrets.prod $BASE_DIR/admin/WMAgent.secrets
    ln -s $BASE_DIR/admin/WMAgent.secrets.prod $DEPLOY_DIR/admin/wmagent/WMAgent.secrets
}

function init()
{
    echo " "
    echo "Running init"
    echo " "

    sleep 1

    bash $WMA_DEPLOY_DIR/init.sh
    source $WMA_DEPLOY_DIR/bin/manage-common.sh
    _load_wmasecrets

    declare -A WMCoreVenvVars
    WMCoreVenvVars[TEAM]=$TEAMNAME
    WMCoreVenvVars[WMCORE_CACHE_DIR]=/tmp/$(whoami)
    WMCoreVenvVars[install]=$CURRENT_DIR/install
    WMCoreVenvVars[config]=$CURRENT_DIR/config
    WMCoreVenvVars[manage]=manage
    _WMCoreVenvSet ${!WMCoreVenvVars[@]}
}

function resource-control()
{
    echo " "
    echo "Running resource-control"
    echo " "

    sleep 1

    #Settings for using T0_CH_CERN_Disk
    manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --cms-name=T2_CH_CERN --pnn=T0_CH_CERN_Disk --ce-name=T2_CH_CERN --pending-slots=20000 --running-slots=20000 --plugin=SimpleCondorPlugin
    manage execute-agent wmagent-resource-control --site-name=T0_CH_CERN_Disk --cms-name=T0_CH_CERN_Disk --pnn=T2_CH_CERN --ce-name=T0_CH_CERN_Disk --pending-slots=20000 --running-slots=20000 --plugin=SimpleCondorPlugin
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

}

function tweak-prod-config()
{
    echo " "
    echo "Running tweak-prod-config"
    echo " "

    sleep 1
    sed -i 's+TIER0_CONFIG_FILE+'"/data/tier0/admin/ProdOfflineConfiguration.py"'+' "$config/config.py"
    sed -i "s+config.Agent.teamName = 'REPLACE_TEAM_NAME'+config.Agent.teamName = '"$TEAMNAME"'+" "$config/config.py"
    sed -i "s+config.Agent.contact = 'cms-comp-ops-workflow-team@cern.ch'+config.Agent.contact = 'cms-tier0-operations@cern.ch'+" "$config/config.py"
    sed -i "s+'team1,team2,cmsdataops'+'tier0production'+g" "$config/config.py"
    sed -i "s+config.RucioInjector.containerDiskRuleParams.*+config.RucioInjector.containerDiskRuleParams = {}+" "$config/config.py"
    echo "config.RucioInjector.blockRuleParams = {}" >> $config/config.py
    sed -i "s+config.RucioInjector.metaDIDProject.*+config.RucioInjector.metaDIDProject = 'Tier0'+" "$config/config.py"
    echo "config.RucioInjector.blockDeletionDelayHours = 168" >> $config/config.py
    echo 'config.BossAir.pluginNames = ["SimpleCondorPlugin"]' >> $config/config.py
    echo 'config.JobAccountant.maxAllowedRepackOutputSize = 24 * 1024 * 1024 * 1024' >> $config/config.py
    echo "config.AgentStatusWatcher.runningExpressPercent = 25" >> $config/config.py
    echo "config.AgentStatusWatcher.runningRepackPercent = 10" >> $config/config.py
    echo 'config.TaskArchiver.archiveDelayHours = 720' >> $config.py
    echo "config.DBS3Upload.datasetType = 'VALID'" >> $config/config.py
    echo "config.Tier0Feeder.serviceProxy = '$DEPLOY_DIR/certs/myproxy.pem'" >> $config/config.py
    echo 'config.TaskArchiver.dashBoardUrl = "http://dashb-luminosity.cern.ch/dashboard/request.py/putluminositydata"' >> $config/config.py
    sed -i "s+config.DBS3Upload.uploaderName = 'WMAgent'+config.DBS3Upload.uploaderName = 'T0Prod'+g" "$config/config.py"
    sed -i "s/config.ErrorHandler.maxFailTime.*/config.ErrorHandler.maxFailTime=601200/g" "$config/config.py"
    sed -i "s+config.AgentStatusWatcher.ignoreDisks.*+config.AgentStatusWatcher.ignoreDisks = [ '/cvmfs/cvmfs-config.cern.ch', '/cvmfs/cms.cern.ch', '/eos/cms', '/cvmfs/cms-ib.cern.ch', '/cvmfs/patatrack.cern.ch' ]+" "$config/config.py"

}

function tweak-replay-config()
{
    echo " "
    echo "Running tweak-replay-config"
    echo " "

    sleep 1

    echo "Modifying config file"
    sed -i 's+TIER0_CONFIG_FILE+'"/data/tier0/admin/ReplayOfflineConfiguration.py"'+' "$config/config.py"
    sed -i "s+config.Agent.teamName = 'REPLACE_TEAM_NAME'+config.Agent.teamName = '"$TEAMNAME"'+" "$config/config.py"
    sed -i "s+config.Agent.contact = 'cms-comp-ops-workflow-team@cern.ch'+config.Agent.contact = 'cms-tier0-operations@cern.ch'+" "$config/config.py"
    sed -i "s+'team1,team2,cmsdataops'+'tier0replay'+g" "$config/config.py"
    sed -i "s+config.RucioInjector.containerDiskRuleParams.*+config.RucioInjector.containerDiskRuleParams = {'lifetime': 7 * 24 * 60 * 60}+" "$config/config.py"
    echo "config.RucioInjector.blockRuleParams = {'lifetime': 7 * 24 * 60 * 60}" >> "$config/config.py"
    sed -i "s+config.RucioInjector.metaDIDProject.*+config.RucioInjector.metaDIDProject = 'Test'+" "$config/config.py"
    echo "config.RucioInjector.blockDeletionDelayHours = 2" >> $config/config.py
    echo "config.DBS3Upload.datasetType = 'VALID'" >> $config/config.py
    echo "config.Tier0Feeder.serviceProxy = '$DEPLOY_DIR/certs/myproxy.pem'" >> $config/config.py
    echo 'config.TaskArchiver.dashBoardUrl = "http://dashb-luminosity.cern.ch/dashboard/request.py/putluminositydata"' >> $config/config.py
    sed -i "s+config.DBS3Upload.uploaderName = 'WMAgent'+config.DBS3Upload.uploaderName = 'T0Replay'+g" "$config/config.py"
    sed -i "s/config.ErrorHandler.maxFailTime.*/config.ErrorHandler.maxFailTime=601200/g" "$config/config.py"
    sed -i "s+config.RucioInjector.listTiersToInject.*+config.RucioInjector.listTiersToInject = ['AOD', 'MINIAOD', 'NANOAOD', 'NANOAODSIM', 'RAW', 'FEVT', 'USER', 'ALCARECO', 'ALCAPROMPT','DQMIO','RAW-RECO']+" "$config/config.py"
    sed -i "s/config.RetryManager.plugins.*/config.RetryManager.plugins={'default': 'PauseAlgo', 'Cleanup': 'PauseAlgo', 'LogCollect': 'PauseAlgo'}/g" "$config/config.py"
    sed -i "s/config.ErrorHandler.maxRetries.*/config.ErrorHandler.maxRetries={'default': 30, 'Cleanup': 30, 'LogCollect': 30}/g" "$config/config.py"
    sed -i "s+config.AgentStatusWatcher.ignoreDisks.*+config.AgentStatusWatcher.ignoreDisks = [ '/cvmfs/cvmfs-config.cern.ch', '/cvmfs/cms.cern.ch', '/eos/cms', '/cvmfs/cms-ib.cern.ch', '/cvmfs/patatrack.cern.ch' ]+" "$config/config.py"

}

function configure-dropbox()
{
    echo " "
    echo "Running configure-dropbox"
    echo " "

    sleep 1 

    DROPBOX_USER=`cat $WMA_SECRETS_FILE | grep DROPBOX_USER | sed s/DROPBOX_USER=//`
    DROPBOX_PASS=`cat $WMA_SECRETS_FILE | grep DROPBOX_PASS | sed s/DROPBOX_PASS=//`

    if [ "x$DROPBOX_USER" == "x" ] || [ "x$DROPBOX_PASS" == "x" ]; then
        echo "Secrets file doesn't contain DROPBOX_USER or DROPBOX_PASS";
        exit 1
    fi

    echo 'config.Tier0Feeder.dropboxuser = "'$DROPBOX_USER'"' >> $config/config.py
    echo 'config.Tier0Feeder.dropboxpass = "'$DROPBOX_PASS'"' >> $config/config.py

}

function configure-rucio()
{
    echo " "
    echo "Running configure-rucio"
    echo " "

    sleep 1

    sed -i "s+rucio_host = RUCIO_HOST_OVERWRITE+rucio_host = ${RUCIO_HOST}+" "$RUCIO_CONFIG"
    sed -i "s+auth_host = RUCIO_AUTH_OVERWRITE+auth_host = ${RUCIO_AUTH}+" "$RUCIO_CONFIG"
    echo -e "\n" >> $RUCIO_CONFIG
    echo "account = $RUCIO_ACCOUNT" >> "$RUCIO_CONFIG"
}
