#!/bin/bash
# This script is used by keepalived notify
# 3 states (arguments given by keepalived)
# MASTER:
# replication to replicat, update murder
# FAULT:
# stop cyrus
# BACKUP:
# listen to replicat, no update on murder

TYPE=$1
NAME=$2
STATE=$3

TIME=`date --rfc-3339=seconds`
IMAPD=/tmp/imapd.conf
CYRUS=/tmp/cyrus.conf
cp /etc/imapd.conf $IMAPD
cp /etc/cyrus.conf $CYRUS
case $STATE in
      "MASTER") echo $TIME $STATE >> /var/log/keepalived.log
        sed -i 's/#\(mupdate_server.*\)$/\1/g' $IMAPD
        sed -i 's/sync_log: 0/sync_log: 1/g' $IMAPD
        sed -i 's/#\(sync.*\)$/\1/g' $CYRUS
        sed -i 's/#\(mupdate.*\)$/\1/g' $CYRUS
        cp $IMAPD /etc/imapd.conf
        cp $CYRUS /etc/cyrus.conf
        systemctl restart cyrus-imapd
        exit 0
        ;;
      "FAULT") echo $TIME $STATE >> /var/log/keepalived.log
        systemctl stop cyrus-imapd
        exit 0
        ;;
      "BACKUP") echo $TIME $STATE >> /var/log/keepalived.log
        sed -i 's/\(mupdate_server.*\)$/#\1/g' $IMAPD
        sed -i 's/sync_log: 1/sync_log: 0/g' $IMAPD
        sed -i 's/\(sync.*\)$/#\1/g' $CYRUS
        sed -i 's/\(mupdate.*\)$/#\1/g' $CYRUS
        cp $IMAPD /etc/imapd.conf
        cp $CYRUS /etc/cyrus.conf
      systemctl start cyrus-imapd
                  exit 0
                  ;;

        *) echo $TIME $STATE >> /var/log/keepalived.log
        echo "unknown state"
        exit 1
        ;;
esac
