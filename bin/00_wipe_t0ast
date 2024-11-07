#!/bin/bash

#Read the connection data from the secrets file

HOME="/data/tier0/admin"

if [ "x$WMAGENT_SECRETS_LOCATION" == "x" ]; then
    WMAGENT_SECRETS_LOCATION=$HOME/WMAgent.secrets;
fi
if [ ! -e $WMAGENT_SECRETS_LOCATION ]; then
    echo "Password file: $WMAGENT_SECRETS_LOCATION does not exist"
    echo "Either set WMAGENT_SECRETS_LOCATION to a valid file or check that $HOME/WMAgent.secrets exists"
    exit 1;
fi

ORACLE_USER=`cat $WMAGENT_SECRETS_LOCATION | grep ORACLE_USER | sed s/ORACLE_USER=//`
ORACLE_PASS=`cat $WMAGENT_SECRETS_LOCATION | grep ORACLE_PASS | sed s/ORACLE_PASS=//`
ORACLE_TNS=`cat $WMAGENT_SECRETS_LOCATION | grep ORACLE_TNS | sed s/ORACLE_TNS=//`

if [ "x$ORACLE_USER" == "x" ] || [ "x$ORACLE_PASS" == "x" ] || [ "x$ORACLE_TNS" == "x" ]; then
    echo "Secrets file doesn't contain ORACLE_USER, ORACLE_PASS or ORACLE_TNS";
    exit 1
fi

echo $ORACLE_USER

PROD_NODES=("vocms0502.cern.ch" "vocms015.cern.ch" "vocms0314.cern.ch" "vocms0313.cern.ch" "vocms014.cern.ch" "vocms013.cern.ch")
HOSTNAME=$(hostname)

if [[ " ${PROD_NODES[@]} " =~ " ${HOSTNAME} " ]]; then
    #Wipe the T0AST
    echo "This is a production node. I must ask again before moving forward..."
    while true; do
        read -p "Would you like to wipe T0AST instance $ORACLE_USER (y/n)? " yn
        case $yn in
        [Y/y]* ) DATA1=true; break;;
        [N/n]* ) DATA1=false; break;;
        * ) echo "Please answer yes or no.";;
        esac
    done
    if [ "$DATA1" == true ]; then
        echo "Wiping T0AST instance $ORACLE_USER"
        sqlplus64 $ORACLE_USER/$ORACLE_PASS@$ORACLE_TNS < /data/tier0/admin/OracleReset.sql
    else
        echo "Not wiping T0AST instance $ORACLE_USER instance. "
        exit 1;
    fi
    
else
    echo "This is a replay node. No fear if you mess up... Wiping T0AST replay"
    sqlplus $ORACLE_USER/$ORACLE_PASS@$ORACLE_TNS < /data/tier0/admin/OracleReset.sql
fi
