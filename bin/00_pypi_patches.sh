#!/bin/bash

# Keeping this as a separate script intentionally to avoid complexity in the deployment script.
# PLEASE CHECK T0 TWIKI COOKBOOK TO SEE MORE INFORMATION ABOUT PATCHING THE T0 WMAGENT

BASE_DIR=/data/tier0
DEPLOY_DIR=$BASE_DIR/WMAgent.venv3

#Dummy demonstrative Patch for new alma 9 agent
curl https://patch-diff.githubusercontent.com/raw/dmwm/T0/pull/4961.patch | patch -d $WMA_DEPLOY_DIR/lib/python3.9/site-packages/ -p 3
