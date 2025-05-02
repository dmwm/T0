#!/bin/bash

# Keeping this as a separate script intentionally to avoid complexity in the deployment script.
# PLEASE CHECK T0 TWIKI COOKBOOK TO SEE MORE INFORMATION ABOUT PATCHING THE T0 WMAGENT

BASE_DIR=/data/tier0
DEPLOY_DIR=$BASE_DIR/WMAgent.venv3

##################
### T0 patches ###
##################

#Dummy demonstrative Patch for new alma 9 agent
#curl https://patch-diff.githubusercontent.com/raw/dmwm/T0/pull/4961.patch | patch -f -d $WMA_DEPLOY_DIR/lib/python3.9/site-packages/ -p 3
#curl https://patch-diff.githubusercontent.com/raw/germanfgv/WMCore/pull/16.patch | patch -f -d $WMA_DEPLOY_DIR/lib/python3.9/site-packages/ -p 3

#Nano Flavours
#curl https://patch-diff.githubusercontent.com/raw/dmwm/T0/pull/5031.patch | patch -f -d $WMA_DEPLOY_DIR/lib/python3.9/site-packages/ -p 3

#Raw skims
#curl https://patch-diff.githubusercontent.com/raw/dmwm/T0/pull/5041.patch | patch -f -d $WMA_DEPLOY_DIR/lib/python3.9/site-packages/ -p 3


######################
### WMCore patches ###
######################

# On top of 2.3.5
## xrdcp exit code capture by Andrea Piccineli

bash $WMA_DEPLOY_DIR/bin/patchComponent.sh 12058 

