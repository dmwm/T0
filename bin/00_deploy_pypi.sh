#!/bin/bash

# Uses:
# * 00_reset_couch.sh
# * deploy-wmagent-venv.sh

WMAGENT_TAG=2.3.3
COUCH_TAG=3.2.2
TIER0_VERSION=3.2.0

BASE_DIR=/data/tier0
DEPLOY_DIR=$BASE_DIR/WMAgent.venv3

WMAGENT_SECRETS=$BASE_DIR/admin/WMAgent.secrets.replay
CERT=/data/certs/robot-cert-cmst0.pem
KEY=/data/certs/robot-key-cmst0.pem

echo "Resetting couchdb for new deployment"
sleep 3
bash $BASE_DIR/00_reset_couch.sh -t $COUCH_TAG

cd $BASE_DIR

echo "Removing deploy directory"
rm -rf $DEPLOY_DIR

echo "Deploying new wmagent"
echo "WMAgent version $WMAGENT_TAG"
echo "Tier0 version $TIER0_VERSION"
sleep 3
./deploy-wmagent-venv.sh -t $WMAGENT_TAG -d $DEPLOY_DIR -y -s

cd $DEPLOY_DIR

echo "Activating virtual environment"
sleep 3
source $DEPLOY_DIR/bin/activate
# Now we have access to WMAgent environment variables

echo "Installing T0"
sleep 3
pip install T0==$TIER0_VERSION

#############################################
### THIS STEP SHOULD HAPPEN AUTOMATICALLY ###
#############################################

echo "Setting up secrets file"
sleep 3
cp $WMAGENT_SECRETS $DEPLOY_DIR/admin/wmagent/WMAgent.secrets

echo "Setting up certificate and key"
sleep 3
cp $CERT $DEPLOY_DIR/certs/servicecert.pem
cp $KEY $DEPLOY_DIR/certs/servicekey.pem

echo "Deployment finished. Now deactivating environment"
sleep 3

echo "activating additional environment variables"
source $WMA_ENV_FILE

deactivate

cd $BASE_DIR



