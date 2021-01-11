#!/bin/bash
# 20.06.2011 - JJaritsch @ ANEXIA Internetdienstleistungs GmbH
# jj@anexia.at

queuelength=`/usr/sbin/postqueue -p | tail -n1 | awk '{print $5}'`
queuecount=`echo $queuelength | grep "[0-9]"`

if [ "$queuecount" == "" ]; then
        echo 0;
else
        echo ${queuelength};
fi
exit 35
