#!/bin/bash

# Uses:
# * 00_reset_couch.sh
# * deploy-wmagent-venv.sh
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

WMAGENT_TAG=2.3.3
COUCH_TAG=3.2.2

BASE_DIR=/data/tier0
SPEC_DIR=/data/tier0/admin/Specs
DEPLOY_DIR=$BASE_DIR/WMAgent.venv3

echo "Resetting couchdb for new deployment"
sleep 3
bash $BASE_DIR/00_reset_couch.sh -t $COUCH_TAG

cd $BASE_DIR

echo "Removing deploy directory"
sleep 3
rm -rf $DEPLOY_DIR

echo "Clearing Specs directory"
sleep 3
rm -rf $SPEC_DIR

echo "Clearing Oracle Database"
sleep 3
bash /data/tier0/00_wipe_t0ast.sh

echo "Installing new wmagent"
echo "WMAgent version $WMAGENT_TAG"
sleep 3

./deploy-wmagent-venv.sh -t $WMAGENT_TAG -d $DEPLOY_DIR -y -s





