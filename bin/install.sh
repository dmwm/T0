#!/bin/bash 

BASE_DIR=/data/tier0
DEPLOY_DIR=$BASE_DIR/WMAgent.venv3
CURRENT_DIR=$DEPLOY_DIR/srv/wmagent/$WMAGENT_TAG

VM_CERTS_DIR=/data/certs
CERT=robot-cert-cmst0.pem
KEY=robot-key-cmst0.pem
PROXY=robot-proxy-vocms001.pem

WMA_VENV_DEPLOY_SCRIPT=https://raw.githubusercontent.com/dmwm/WMCore/$WMAGENT_TAG/deploy/deploy-wmagent-venv.sh

while getopts "t:w:" opt; do
    case $opt in
        t) 
            T0_TAG=$OPTARG ;;
        w)
            WMAGENT_TAG=$OPTARG ;;
    esac
done

function install-wmagent()
{
    rm $BASE_DIR/deploy-wmagent-venv.sh
    wget $WMA_VENV_DEPLOY_SCRIPT -O $BASE_DIR/deploy-wmagent-venv.sh
    sed -i 's|\$WMA_CERTS_DIR/myproxy.pem|\$WMA_CERTS_DIR/robot-proxy-vocms001.pem|g' $BASE_DIR/deploy-wmagent-venv.sh
    bash $BASE_DIR/deploy-wmagent-venv.sh -t $WMAGENT_TAG -d $DEPLOY_DIR -p /usr/bin/python3.12 -y
    source $DEPLOY_DIR/bin/activate
}

function configure-certs()
{

    cp $VM_CERTS_DIR/$CERT $WMA_CERTS_DIR
    cp $VM_CERTS_DIR/$KEY $WMA_CERTS_DIR
    cp $VM_CERTS_DIR/$PROXY $WMA_CERTS_DIR

    ln -s $WMA_CERTS_DIR/$CERT $WMA_CERTS_DIR/servicecert.pem
    ln -s $WMA_CERTS_DIR/$KEY $WMA_CERTS_DIR/servicekey.pem
    ln -s $WMA_CERTS_DIR/$PROXY $WMA_CERTS_DIR/myproxy.pem

}

function install-t0()
{
    pip install T0==$T0_TAG
    chmod +x $DEPLOY_DIR/bin/t0
}

function patch-agent()
{
    bash $BASE_DIR/patch.sh
}

function main()
{
    cd $BASE_DIR
    install-wmagent
    configure-certs
    install-t0
    patch-agent
}
