#!/bin/bash

# Keeping this as a separate script intentionally to avoid complexity in the deployment script.
# PLEASE CHECK T0 TWIKI COOKBOOK TO SEE MORE INFORMATION ABOUT PATCHING THE T0 WMAGENT

BASE_DIR=/data/tier0
DEPLOY_DIR=$BASE_DIR/WMAgent.venv3

##################
### T0 patches ###
##################

#Dummy demonstrative Patch for new alma 9 agent
#curl https://patch-diff.githubusercontent.com/raw/dmwm/T0/pull/4961.patch | patch -f -d $WMA_DEPLOY_DIR/lib/python3.12/site-packages/ -p 3

######################
### WMCore patches ###
######################


# On top of 2.3.5

# RetryManager bug fix
curl https://patch-diff.githubusercontent.com/raw/Viphava280444/WMCore/pull/1.patch | patch -f -d $WMA_DEPLOY_DIR/lib/python3.12/site-packages/ -p 3

# JobSubmitter patch for older jobs to have higher priority
curl https://patch-diff.githubusercontent.com/raw/LinaresToine/WMCore/pull/21.patch | patch -f -d $WMA_DEPLOY_DIR/lib/python3.12/site-packages/ -p 3

#Alca harvest PFN fix
bash $WMA_DEPLOY_DIR/bin/patchComponent.sh 12478
