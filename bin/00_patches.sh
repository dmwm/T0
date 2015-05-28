#!/bin/bash

BASE_DIR=/data/tier0
DEPLOY_DIR=$BASE_DIR/srv/wmagent

. $DEPLOY_DIR/current/apps/t0/etc/profile.d/init.sh

#cd /data/hufnagel/WMCore
# options are
# wmc-web, wmc-base, reqmon, crabserver, wmclient, wmc-component, crabclient, wmc-database, wmc-runtime, wmagent, workqueue, reqmgr, asyncstageout
#wmc-dist-unpatch
#wmc-dist-patch -s wmc-base
#wmc-dist-patch -s wmc-database
#wmc-dist-patch -s wmc-component
#wmc-dist-patch -s wmagent

cd $BASE_DIR/WMCore

rm -rf $WMAGENT_ROOT/lib
python setup.py clean
python setup.py build
#python setup.py test
python setup.py install --prefix=$WMAGENT_ROOT

cd $BASE_DIR/T0

rm -rf $T0_ROOT/lib
python setup.py clean
python setup.py build
#python setup.py test
python setup.py install --prefix=$T0_ROOT

