#!/bin/bash

log=/home/geekfest/geekstats/logs/geekstats.log
timestamp=`date "+%Y-%m-%d %H:%M:%S"`

echo ""
echo -n "Stopping any running GeekSTATS listeners.................."
pkill -f loglistenerdaemon.py
echo " [DONE]"
echo ""

echo -n "Starting the GeekSTATS listener in background............."
echo -n "$timestamp : [GEEKSTATS] " > $log
/usr/bin/python -u /home/geekfest/geekstats/github/geekstats/logprocessor/loglistenerdaemon.py >> $log &
echo " [DONE]"
echo ""

