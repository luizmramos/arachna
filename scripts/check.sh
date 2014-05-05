#!/bin/bash
[ "`service arachna status | grep -c not`" = 1 ] && sudo service arachna start && echo "`date +%Y%m%d%H%M`" >> /Arachna/logs/server/down.log
