#!/bin/bash

BASE_DIR=/data/tier0

rm -rf $BASE_DIR/WMCore
cd $BASE_DIR
git clone https://github.com/dmwm/WMCore.git 

cd $BASE_DIR/WMCore

git checkout tags/1.0.7.pre6

# enable lazydownload
# (wait for pull request to be merged)
git fetch https://github.com/hufnagel/WMCore enable-lazydownload && git cherry-pick FETCH_HEAD

# enable xrootd debug output
# (for testing only)
git fetch https://github.com/hufnagel/WMCore xrootd-debug && git cherry-pick FETCH_HEAD

# overcommit multicore pilots
git fetch https://github.com/hufnagel/WMCore overcommit-pilot && git cherry-pick FETCH_HEAD

# fix for phedex recovery
git fetch https://github.com/hufnagel/WMCore phedex-recovery-limits && git cherry-pick FETCH_HEAD

rm -rf $BASE_DIR/T0
cd $BASE_DIR
git clone https://github.com/dmwm/T0.git

cd $BASE_DIR/T0

git checkout tags/1.9.94

# map out known corrupt Run2012 replay streamer
git fetch https://github.com/hufnagel/T0 zeroevents && git cherry-pick FETCH_HEAD

# remove TFC override, read streamer from EOS
git fetch https://github.com/hufnagel/T0 remove-tfc-override && git cherry-pick FETCH_HEAD

