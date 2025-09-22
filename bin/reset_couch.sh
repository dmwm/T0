#!/bin/bash

COUCH_TAG=''
while getopts ":t:" opt; do
    case $opt in
        t) COUCH_TAG=$OPTARG ;;
    esac
done

sleep 3
COUCH_DIR=/data/CMSKubernetes/docker/pypi/wmagent-couchdb
cd $COUCH_DIR

echo "Killing any existing couchdb container"
sleep 3
if docker ps -a --format '{{.Names}}' | grep -q "couchdb"; then
    docker kill couchdb
fi

echo "Running new couch container"
if [ -z "$COUCH_TAG" ]; then
    bash $COUCH_DIR/couchdb-docker-run.sh -p
else
    bash $COUCH_DIR/couchdb-docker-run.sh -t $COUCH_TAG -p
fi




