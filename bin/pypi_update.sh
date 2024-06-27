#!/bin/bash

BASE_DIR=/data/tier0
cd $BASE_DIR

echo "Removing old scripts"
sleep 1
rm $BASE_DIR/00_pypi_*.sh
sleep 1

declare -A PYPI_DEPLOYMENT_SCRIPTS=(
    [00_pypi_start_agent.sh]=https://raw.githubusercontent.com/dmwm/T0/master/bin/00_pypi_start_agent.sh
    [00_pypi_stop_agent.sh]=https://raw.githubusercontent.com/dmwm/T0/master/bin/00_pypi_stop_agent.sh
    [00_pypi_reset_couch.sh]=https://raw.githubusercontent.com/dmwm/T0/master/bin/00_pypi_reset_couch.sh
    [00_pypi_resource_control.sh]=https://raw.githubusercontent.com/dmwm/T0/master/bin/00_pypi_resource_control.sh
    [00_pypi_patches.sh]=https://raw.githubusercontent.com/dmwm/T0/master/bin/00_pypi_patches.sh
    [00_pypi_deploy_replay.sh]=https://raw.githubusercontent.com/dmwm/T0/master/bin/00_pypi_deploy_replay.sh
    [00_pypi_deploy_prod.sh]=https://raw.githubusercontent.com/dmwm/T0/master/bin/00_pypi_deploy_prod.sh
    [00_pypi_tweak_replay_config.sh]=https://raw.githubusercontent.com/dmwm/T0/master/bin/00_pypi_tweak_replay_config.sh
    [00_pypi_tweak_prod_config.sh]=https://raw.githubusercontent.com/dmwm/T0/master/bin/00_pypi_tweak_prod_config.sh
)

for SCRIPT in "${!PYPI_DEPLOYMENT_SCRIPTS[@]}"; do
    echo "Now updating $SCRIPT"
    sleep 1
    wget ${PYPI_DEPLOYMENT_SCRIPTS[$SCRIPT]} -O $BASE_DIR/$SCRIPT
    chmod +x $BASE_DIR/$SCRIPT
done

