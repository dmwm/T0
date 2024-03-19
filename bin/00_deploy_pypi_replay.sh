#!/bin/bash

BASE_DIR=/data/tier0
COUCHDB_DOCKER_DIR=$BASE_DIR/dockerMount/CMSKubernetes.couchdb/docker/pypi/wmagent-couchdb
DEPLOY_DIR=$BASE_DIR/WMAgent.venv3
WMAGENT_SECRETS=$BASE_DIR/admin/WMAgent.secrets.replay
CERT=/data/certs/robot-cert-cmst0.pem
KEY=/data/certs/robot-key-cmst0.pem
#SPEC_DIR=$BASE_DIR/admin/Specs

WMAGENT_TAG=2.3.0
COUCHDB_TAG=3.2.2
TIER0_VERSION=3.1.5
#TIER0_ARCH=slc7_amd64_gcc630
#DEPLOY_TAG=HG2402a
cd $BASE_DIR
echo "Removing deploy directory"
rm -rf $DEPLOY_DIR

echo "Deploying new wmagent"
echo "WMAgent version $WMAGENT_TAG"
echo "Tier0 version $TIER0_VERSION"
sleep 3
./deploy-wmagent-venv.sh -t $WMAGENT_TAG -y -s

cd $DEPLOY_DIR

echo "Activating virtual environment"
sleep 3
source $DEPLOY_DIR/bin/activate

echo "wiping t0ast"
sleep 3
$BASE_DIR/00_wipe_t0ast.sh 2>&1 > /dev/null

### Temporary files for proper initialization of the agent ###
### These should be updated and included properly ###
#######################################################
cp $BASE_DIR/init.sh $DEPLOY_DIR/init.sh
cp $BASE_DIR/manage-common.sh $DEPLOY_DIR/bin/manage-common.sh
cp $BASE_DIR/config.py $WMA_CONFIG_DIR/config.py           
#######################################################

export WMAGENT_SECRETS_LOCATION=$WMA_SECRETS_FILE
export config=$WMA_CONFIG_DIR/config.py
echo "Setting up secrets file"
sleep 3
ln -s $WMAGENT_SECRETS $DEPLOY_DIR/admin/wmagent/WMAgent.secrets

echo "Setting up certificate and key"
sleep 3
ln -s $CERT $DEPLOY_DIR/certs/servicecert.pem
ln -s $KEY $DEPLOY_DIR/certs/servicekey.pem

echo "Synchronizing pycurl link time and compile time backend to openssl"
sleep 3
pip uninstall pycurl
export PYCURL_SSL_LIBRARY=openssl
pip install --no-cache-dir --global-option=build_ext --global-option="-L/usr/local/opt/openssl/lib" --global-option="-I/usr/local/opt/openssl/include"  pycurl

echo "Setting up couchdb container"
sleep 3
if docker ps -a --format '{{.Names}}' | grep -q "couchdb"; then
    docker kill couchdb
else
    echo "Container does not exist"
fi
cd $COUCHDB_DOCKER_DIR
./couchdb-docker-build.sh $COUCHDB_TAG
./couchdb-docker-run.sh $COUCHDB_TAG
docker exec couchdb manage pushapps

echo "sourcing manage-common.sh to enable database related functions"
source $DEPLOY_DIR/bin/manage-common.sh

cd $DEPLOY_DIR
_load_wmasecrets

echo "Now initializing"
sleep 3
$DEPLOY_DIR/init.sh

echo "stop and start agent"
manage stop-agent
manage start-agent


