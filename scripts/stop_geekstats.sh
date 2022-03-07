#!/bin/bash

log=/home/geekfest/geekstats/logs/geekstats.log
timestamp=`date "+%Y-%m-%d %H:%M:%S"`

echo ""
echo -n "Stopping any running GeekSTATS listeners.................."
pkill -f loglistenerdaemon.py
echo " [DONE]"
echo -n "$timestamp : [GEEKSTATS] Listener Stopped" >> $log
echo ""
