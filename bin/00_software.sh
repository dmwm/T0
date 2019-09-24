#!/bin/bash

BASE_DIR=/data/tier0
WMCORE_VERSION=1.1.20.patch4
T0_VERSION=2.1.4

function echo_header {
	echo ''
	echo " *** $1 *** "
}

echo_header 'Cloning WMCore'
rm -rf $BASE_DIR/WMCore
cd $BASE_DIR
git clone https://github.com/dmwm/WMCore.git

cd $BASE_DIR/WMCore

echo_header "Switching to tag $WMCORE_VERSION"
git checkout tags/$WMCORE_VERSION

########################################
# Mandatory WMCore patches
########################################

echo_header 'Applying WMCore mandatory patches'

#Skip WorkQueue MonIT statistics for T0 agent
git fetch https://github.com/amaltaro/WMCore fix-9056 && git cherry-pick FETCH_HEAD

#Use `tier0_wmagent` producer for T0 agent uploading data to MonIT
git fetch https://github.com/amaltaro/WMCore tier0-producer && git cherry-pick FETCH_HEAD

#Change default AMQ host and ports:
git fetch https://github.com/vytjan/WMCore default-amq-hostname && git cherry-pick FETCH_HEAD
########################################
# Additional (Optional) WMCore patches
########################################

echo_header 'Applying WMCore optional patches'

# Allow not failing job creation in JobSplitting/ EventAwareLumiBased if specified in WMAgent config
git fetch https://github.com/khurtado/WMCore jobsplitnewat && git cherry-pick FETCH_HEAD

# enable xrootd debug output
# (for testing only)
# git fetch https://github.com/hufnagel/WMCore xrootd-debug && git cherry-pick FETCH_HEAD

########################################

echo_header 'Cloning T0'
rm -rf $BASE_DIR/T0
cd $BASE_DIR
git clone https://github.com/dmwm/T0.git

cd $BASE_DIR/T0

echo_header "Switching to tag $T0_VERSION"
git checkout tags/$T0_VERSION

########################################
# Mandatory T0 patches
########################################

echo_header 'Applying T0 mandatory patches'

#Move SMNOTIFYDB_URL to secrets file
git fetch https://github.com/vytjan/T0 smnotifydb-to-secrets && git cherry-pick FETCH_HEAD
########################################
# Additional (Optional) T0 patches
########################################

echo_header 'Applying T0 optional patches'

########################################
