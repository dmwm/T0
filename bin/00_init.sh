#!/bin/bash 

DEPLOY_DIR=/data/tier0/WMAgent
cd $DEPLOY_DIR
echo "Activating WMAgent virtual environment"
sleep 3
source $DEPLOY_DIR/bin/activate

echo "Cleaning T0AST database"
sleep 3
manage clean-oracle

echo "Now initializing"
bash $DEPLOY_DIR/init.sh



