#!/bin/bash

echo "Activating WMAgent environment"
sleep 3
WMAGENT_DIR=/data/tier0/WMAgent.venv3
cd $WMAGENT_DIR
source $WMAGENT_DIR/bin/activate

echo "Now stopping the agent"
sleep 3

manage stop-agent

echo "Deactivating WMAgent environment"
deactivate


