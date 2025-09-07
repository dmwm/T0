#!/bin/bash

BASE_DIR=/data/tier0
cd $BASE_DIR

echo "Removing old scripts"
sleep 1
rm $BASE_DIR/00_pypi_*.sh
sleep 1

declare -A DEPLOYMENT_SCRIPTS=(
    [install.sh]=https://raw.githubusercontent.com/dmwm/T0/master/bin/install.sh
    [deploy.sh]=https://raw.githubusercontent.com/dmwm/T0/master/bin/deploy.sh
    [patch.sh]=https://raw.githubusercontent.com/dmwm/T0/master/bin/patch.sh
    [reset_couch.sh]=https://raw.githubusercontent.com/dmwm/T0/master/bin/reset_couch.sh
)

for SCRIPT in "${!DEPLOYMENT_SCRIPTS[@]}"; do
    echo "Now updating $SCRIPT"
    sleep 1
    wget ${PYPI_DEPLOYMENT_SCRIPTS[$SCRIPT]} -O $BASE_DIR/$SCRIPT
    chmod +x $BASE_DIR/$SCRIPT
done

