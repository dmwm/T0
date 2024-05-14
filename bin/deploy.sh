###

BASE_DIR=/data/tier0
SPEC_DIR=$BASE_DIR/admin/Specs

TIER0_VERSION=3.1.6
WMA_VERSION=2.3.3

DEPLOY_DIR=$BASE_DIR/WMAgent.venv3/$WMA_VERSION


# Deploy WMAgent
$BASE_DIR/deploy-wmagent-venv -y -t $WMA_VERSION -d $DEPLOY_DIR -s
cd $DEPLOY_DIR

# Activate environment
./bin/activate

# Installing t0
pip install t0=$TIER0_VERSION

# Copying certs (Change to sym links?)
cp /data/certs/* ./certs
cp /data/tier0/admin/WMAgent.secrets


# It will fail, but it is needed for now
./init.sh

# Clean oracle
manage clean-oracle

# Initialization of the agent
./init.sh

### run manage functions from terminal
source bin/manage-common.sh