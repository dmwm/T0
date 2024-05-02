#!/bin/bash

# Keeping this as a separate script intentionally to avoid complexity in the deployment script.
# PLEASE CHECK T0 TWIKI COOKBOOK TO SEE MORE INFORMATION ABOUT PATCHING THE T0 WMAGENT

BASE_DIR=/data/tier0
DEPLOY_DIR=$BASE_DIR/srv/wmagent

#Emulated data handling
curl https://patch-diff.githubusercontent.com/raw/dmwm/T0/pull/4921.patch | patch -d $DEPLOY_DIR/current/apps/t0/lib/python3.8/site-packages/ -p 3

#Fix cmsRun logs
curl https://patch-diff.githubusercontent.com/raw/dmwm/WMCore/pull/11933.patch | patch -d $DEPLOY_DIR/current/apps/t0/lib/python3.8/site-packages/ -p 3

#Repack data tiers
curl https://patch-diff.githubusercontent.com/raw/dmwm/T0/pull/4926.patch | patch -d $DEPLOY_DIR/current/apps/t0/lib/python3.8/site-packages/ -p 3

#L1SCOUT support in WMCore
curl https://patch-diff.githubusercontent.com/raw/dmwm/WMCore/pull/11930.patch | patch -d $DEPLOY_DIR/current/apps/t0/lib/python3.8/site-packages/ -p 3
curl https://patch-diff.githubusercontent.com/raw/dmwm/WMCore/pull/11951.patch | patch -d $DEPLOY_DIR/current/apps/t0/lib/python3.8/site-packages/ -p 3
curl https://patch-diff.githubusercontent.com/raw/dmwm/WMCore/pull/11952.patch | patch -d $DEPLOY_DIR/current/apps/t0/lib/python3.8/site-packages/ -p 3

#Add extra mapping for repack
curl https://patch-diff.githubusercontent.com/raw/dmwm/T0/pull/4945.patch | patch -d $DEPLOY_DIR/current/apps/t0/lib/python3.8/site-packages/ -p 3
