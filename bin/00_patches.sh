#!/bin/bash

# Keeping this as a separate script intentionally to avoid complexity in the deployment script.
# PLEASE CHECK T0 TWIKI COOKBOOK TO SEE MORE INFORMATION ABOUT PATCHING THE T0 WMAGENT

BASE_DIR=/data/tier0
DEPLOY_DIR=$BASE_DIR/srv/wmagent


#Patches on top of 2.2.4

#wget -nv https://github.com/dmwm/T0/pull/4566.patch -O - | patch -f -d $DEPLOY_DIR/current/apps/t0/lib/python*/site-packages/ -p 3
#wget -nv https://github.com/dmwm/WMCore/pull/10344.patch -O - | patch -f -d $DEPLOY_DIR/current/apps/t0/lib/python*/site-packages/ -p 3
#wget -nv https://github.com/dmwm/T0/pull/4589.patch -O - | patch -f -d $DEPLOY_DIR/current/apps/t0/lib/python*/site-packages/ -p 3
#wget -nv https://github.com/dmwm/T0/pull/4596.patch -O - | patch -f -d $DEPLOY_DIR/current/apps/t0/lib/python*/site-packages/ -p 3
#wget -nv https://github.com/dmwm/T0/pull/4597.patch -O - | patch -f -d $DEPLOY_DIR/current/apps/t0/lib/python*/site-packages/ -p 3

#Patches on top of 3.0.1
wget -nv https://github.com/dmwm/WMCore/pull/10801.patch -O - | patch -f -d $DEPLOY_DIR/current/apps/t0/lib/python3*/site-packages/ -p 3
wget -nv https://github.com/dmwm/T0/pull/4611.patch -O - | patch -f -d $DEPLOY_DIR/current/apps/t0/lib/python3*/site-packages/ -p 3
