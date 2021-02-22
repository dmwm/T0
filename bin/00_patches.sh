#!/bin/bash

# Keeping this as a separate script intentionally to avoid complexity in the deployment script.
# PLEASE CHECK T0 TWIKI COOKBOOK TO SEE MORE INFORMATION ABOUT PATCHING THE T0 WMAGENT

BASE_DIR=/data/tier0
DEPLOY_DIR=$BASE_DIR/srv/wmagent

# Do not allow T0 to use WorkQueue in any case: https://github.com/dmwm/WMCore/pull/9314
curl https://patch-diff.githubusercontent.com/raw/dmwm/WMCore/pull/10044.patch | patch -d $DEPLOY_DIR/current/apps/t0/lib/python2.7/site-packages/ -p3
curl https://patch-diff.githubusercontent.com/raw/dmwm/WMCore/pull/10067.patch | patch -d $DEPLOY_DIR/current/apps/t0/lib/python2.7/site-packages/ -p3
curl https://patch-diff.githubusercontent.com/raw/dmwm/WMCore/pull/10105.patch | patch -d $DEPLOY_DIR/current/apps/t0/lib/python2.7/site-packages/ -p3
