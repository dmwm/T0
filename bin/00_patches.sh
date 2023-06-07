#!/bin/bash

# Keeping this as a separate script intentionally to avoid complexity in the deployment script.
# PLEASE CHECK T0 TWIKI COOKBOOK TO SEE MORE INFORMATION ABOUT PATCHING THE T0 WMAGENT

BASE_DIR=/data/tier0
DEPLOY_DIR=$BASE_DIR/srv/wmagent

#Patches on top of 3.0.7
# Remove py2 compatibility (Needed for #11473)
# curl https://patch-diff.githubusercontent.com/raw/dmwm/WMCore/pull/11420.patch | patch -d $DEPLOY_DIR/current/apps/t0/lib/python3.8/site-packages/ -p 3
# Deprecate TFC override for multi-step jobs
# curl https://patch-diff.githubusercontent.com/raw/dmwm/WMCore/pull/11473.patch | patch -d $DEPLOY_DIR/current/apps/t0/lib/python3.8/site-packages/ -p 3
# Adopt CMS_PATH and SITECONFIG_PATH to locate the site catalog
# curl https://patch-diff.githubusercontent.com/raw/dmwm/WMCore/pull/11481.patch | patch -d $DEPLOY_DIR/current/apps/t0/lib/python3.8/site-packages/ -p 3

#Patches on top of 3.0.8
# Adopt CMS_PATH and SITECONFIG_PATH to locate the site catalog
curl https://patch-diff.githubusercontent.com/raw/dmwm/WMCore/pull/11481.patch | patch -d $DEPLOY_DIR/current/apps/t0/lib/python3.8/site-packages/ -p 3

# Add new CMSCouch exception for Request Entity Too Large
curl https://patch-diff.githubusercontent.com/raw/dmwm/WMCore/pull/11502.patch | patch -d $DEPLOY_DIR/current/apps/t0/lib/python3.8/site-packages/ -p 3

# Add new pp scenario
curl https://patch-diff.githubusercontent.com/raw/dmwm/T0/pull/4813.patch | patch -d $DEPLOY_DIR/current/apps/t0/lib/python3.8/site-packages/ -p 3

#Adding support for writing nano aod
curl https://patch-diff.githubusercontent.com/raw/dmwm/T0/pull/4827.patch | patch -d $DEPLOY_DIR/current/apps/t0/lib/python3.8/site-packages/ -p 3

#Include nanoaod support in Tier0FeederPoller
curl https://patch-diff.githubusercontent.com/raw/dmwm/T0/pull/4836.patch | patch -d $DEPLOY_DIR/current/apps/t0/lib/python3.8/site-packages/ -p 3

