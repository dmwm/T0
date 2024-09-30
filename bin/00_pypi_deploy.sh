#!/bin/bash

### The deployment script must accomplish the following:
# * Ask for confirmation of host machine to deploy in case its a prod node deployment
#
# * Wipe T0AST DB
#    * run 00_wipe_t0ast.sh
# * Clean /data/tier0/admin/Specs directory
# * Clean couchdb data in /data/dockerMount
#
# * Use deploy-wmagent-venv.sh to install the virtual environment and all the required software
#
# * Make sure all certificates and the secrets file is well placed in the corresponding location
#   * certificates
#      * /data/certs 
#         * robot-cert-cmst0.pem
#         * robot-key-cmst0.pem
#         * robot-proxy-vocms001.pem
#         * servicecert.pem --> robot-cert-cmst0.pem
#         * servicekey.pem --> robot-key-cmst0.pem
#         * myproxy.pem --> robot-proxy-vocms001.pem
#      * /data/tier0/WMAgent.venv3/certs
#         * servicecert.pem --> /data/certs/robot-cert-cmst0.pem
#         * servicekey.pem --> /data/certs/robot-key-cmst0.pem
#         * myproxy.pem --> /data/certs/robot-proxy-vocms001.pem
#         * robot-cert-cmst0.pem --> /data/certs/robot-cert-cmst0.pem
#         * robot-key-cmst0.pem --> /data/certs/robot-cert-cmst0.pem
#         * robot-proxy-vocms001.pem --> /data/certs/robot-proxy-vocms001.pem
#   * WMAgent.secrets
#      * /data/tier0/admin/WMAgent.secrets --> /data/tier0/admin/WMAgent.secrets.prod/replay
#      * /data/tier0/WMAgent.venv3/admin/wmagent/WMAgent.secrets --> /data/tier0/admin/WMAgent.secrets.prod/replay
#
# * Activate virtual environment and install T0 code
# * Add useful environment variables for T0
# * Run init.sh
# * Populate resource control
# * Modify config.py

### Usage ###
# To deploy Production Master agent
# * source 00_pypi_deploy.sh -p -m -t -w 

help(){
    echo -e $*
    cat <<EOF
    Usage: source 00_pypi_deploy.sh [-p/r] [-n]
                                    [-t <tier0 version>] 
                                    [-w <wmagent version>]
                                    [-h <help>]

      -p                             Production deployment         [ -p OR -r is required ]
      -r                             Replay deployment             [ -p OR -r is required ]
      -n                             Sets Agent name. Default is MainAgent 
      -s                             Sets Agent as a Slave agent   
      -h <help>                      Provides help to the current script

EOF
}

usage(){
    help $*
    exit 1
}
WMAGENT_TAG=2.3.4
TIER0_VERSION=3.2.3
COUCH_TAG=3.2.2
PROD_AGENT=0
REPLAY_AGENT=0
AGENT_NAME=""

BASE_DIR=/data/tier0
DEPLOY_DIR=$BASE_DIR/WMAgent.venv3
SPEC_DIR=$BASE_DIR/admin/Specs
CONFIGURATION_FILE=''
WMAGENT_SECRETS=''

# Process options


while getopts "prt:w:n:h" opt; do
  case ${opt} in
    p )
        PROD_AGENT=1
        REPLAY_AGENT=0
        CONFIGURATION_FILE='/data/tier0/admin/ProdOfflineConfiguration.py'
        WMAGENT_SECRETS=$BASE_DIR/admin/WMAgent.secrets.prod
        TWEAK_CONFIG_FILE=$BASE_DIR/00_pypi_tweak_prod_config.sh
        ;;
    r )
        REPLAY_AGENT=1
        PROD_AGENT=0
        CONFIGURATION_FILE='/data/tier0/admin/ReplayOfflineConfiguration.py'
        WMAGENT_SECRETS=$BASE_DIR/admin/WMAgent.secrets.replay
        TWEAK_CONFIG_FILE=$BASE_DIR/00_pypi_tweak_replay_config.sh
        ;;
    t )
        TIER0_VERSION=$OPTARG  
        ;;
    w )
        WMAGENT_TAG=$OPTARG  
        ;;
    n )
        AGENT_NAME=$OPTARG
        ;;
    h )
        help
        exit 0
        ;;
    \? )
      echo "Invalid option: -$OPTARG" >&2
      ;;
    : )
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

if (( PROD_AGENT + REPLAY_AGENT != 1 )); then

  echo "Error: Either -p or -r is required. "
  echo "Please use -p flag to deploy production. Use -r flag to deploy replay"
  exit 1

fi

PROD_NODES=("vocms0314.cern.ch" "vocms0313.cern.ch" "vocms014.cern.ch" "vocms013.cern.ch")
HOSTNAME=$(hostname)

if [[ " ${PROD_NODES[@]} " =~ " ${HOSTNAME} " ]]; then
    echo "This is a production node"
    echo "Please name the node you intend to deploy (include .cern.ch : vocms001.cern.ch)"
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
fi

confirm_clearing=""

echo "This will clear the oracle database, couchdb, and important agent directories assosiated to $(hostname)"
cat $WMAGENT_SECRETS | grep "ORACLE_USER"

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

echo "Now deploying WMAgent tag $WMAGENT_TAG with T0 tag $TIER0_VERSION"

CURRENT_DIR=$DEPLOY_DIR/srv/wmagent/$WMAGENT_TAG
CERT=/data/certs/robot-cert-cmst0.pem
KEY=/data/certs/robot-key-cmst0.pem
PROXY=/data/certs/robot-proxy-vocms001.pem
RUCIO_CONFIG=$DEPLOY_DIR/etc/rucio.cfg
RUCIO_HOST=$(grep '^RUCIO_HOST=' $WMAGENT_SECRETS | cut -d'=' -f2)
RUCIO_AUTH=$(grep '^RUCIO_AUTH=' $WMAGENT_SECRETS | cut -d'=' -f2)
RUCIO_ACCOUNT=$(grep '^RUCIO_ACCOUNT=' $WMAGENT_SECRETS | cut -d'=' -f2)
WMA_VENV_DEPLOY_SCRIPT=https://raw.githubusercontent.com/dmwm/WMCore/$WMAGENT_TAG/deploy/deploy-wmagent-venv.sh

function clean_oracle() 
{
    echo "Clearing Oracle Database"
    sleep 3
    bash $BASE_DIR/00_wipe_t0ast.sh
}

function clean_specs()
{
    echo "Clearing Specs directory"
    sleep 3
    rm -rf $SPEC_DIR/*
}

function reset_couch()
{
    echo "Resetting couchdb for new deployment"
    sleep 3
    bash $BASE_DIR/00_pypi_reset_couch.sh -t $COUCH_TAG
}

function set_wmagent_venv()
{
    rm $BASE_DIR/deploy-wmagent-venv.sh
    wget $WMA_VENV_DEPLOY_SCRIPT -O $BASE_DIR/deploy-wmagent-venv.sh
    sed -i 's|\$WMA_CERTS_DIR/myproxy.pem|\$WMA_CERTS_DIR/robot-proxy-vocms001.pem|g' $BASE_DIR/deploy-wmagent-venv.sh
    bash $BASE_DIR/deploy-wmagent-venv.sh -t $WMAGENT_TAG -d $DEPLOY_DIR -y
}

function set_secrets()
{
    echo "Setting up secrets file"
    sleep 1
    rm $DEPLOY_DIR/admin/wmagent/*
    ln -s $WMAGENT_SECRETS $DEPLOY_DIR/admin/wmagent/WMAgent.secrets
}

function activate()
{
    echo "Activating environment"
    sleep 2
    cd $DEPLOY_DIR
    source $DEPLOY_DIR/bin/activate
}

function install_tier0()
{
    echo "Installing T0 code"
    sleep 2
    pip install T0==$TIER0_VERSION
}

function patch()
{
    echo "Applying patches"
    sleep 2
    bash $BASE_DIR/00_pypi_patches.sh
}

function declare_useful_variables()
{
    echo "Now creating important T0 related environment variables"
    sleep 2
    echo "WMCORE_CACHE_DIR=/tmp/cmst0"
    echo "install=$CURRENT_DIR/install"
    echo "config=$CURRENT_DIR/config"
    echo "manage=manage"
    sleep 1

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
}

function init()
{
    echo "Now initializing"
    sleep 2
    bash $DEPLOY_DIR/init.sh
}

function set_certificates()
{
    echo "Setting up certificate and key"
    sleep 1
    rm $DEPLOY_DIR/certs/*
    ln -s $CERT $DEPLOY_DIR/certs/servicecert.pem
    ln -s $KEY $DEPLOY_DIR/certs/servicekey.pem
    ln -s $PROXY $DEPLOY_DIR/certs/myproxy.pem
    ln -s $CERT $DEPLOY_DIR/robot-cert-cmst0.pem
    ln -s $KEY $DEPLOY_DIR/robot-key-cmst0.pem
    ln -s $PROXY $DEPLOY_DIR/robot-proxy-vocms001.pem
}

function resource_control()
{
    echo "Now populating resource control"
    sleep 2
    bash $DEPLOY_DIR/bin/00_pypi_resource_control.sh
}

function tweak_agent_config()
{
    echo 'Now tweaking the config.py file'
    sleep 1
    bash $BASE_DIR/00_pypi_tweak_replay_config.sh $AGENT_NAME
}

function tweak_rucio_config()
{
    sed -i "s+rucio_host = RUCIO_HOST_OVERWRITE+rucio_host = ${RUCIO_HOST}+" "$RUCIO_CONFIG"
    sed -i "s+auth_host = RUCIO_AUTH_OVERWRITE+auth_host = ${RUCIO_AUTH}+" "$RUCIO_CONFIG"
    echo -e "\n" >> $RUCIO_CONFIG
    echo "account = $RUCIO_ACCOUNT" >> "$RUCIO_CONFIG"
}

main()
{
    clean_oracle
    clean_specs
    reset_couch
    set_wmagent_venv
    set_secrets
    activate
    install_tier0
    patch
    declare_useful_variables
    init
    set_certificates
    resource_control
    tweak_agent_config
    tweak_rucio_config
}

main
cd $BASE_DIR