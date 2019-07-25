#!/bin/bash

# Keeping this as a separate script intentionally to avoid complexity in the deployment script.
# PLEASE CHECK T0 TWIKI COOKBOOK TO SEE MORE INFORMATION ABOUT PATCHING THE T0 WMAGENT

BASE_DIR=/data/tier0
DEPLOY_DIR=$BASE_DIR/srv/wmagent

# LogCollect job fix - https://github.com/dmwm/WMCore/pull/9295
# curl https://patch-diff.githubusercontent.com/raw/dmwm/WMCore/pull/9295.patch | patch -d $DEPLOY_DIR/current/apps/t0/lib/python2.7/site-packages/ -p3
