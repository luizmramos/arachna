#!/bin/bash
mv /Arachna/logs/server/log /Arachna/logs/server/`date +%Y%m%d%H`.log
find /Arachna/logs/server/* -mtime +7 -exec rm {} \;
find /Arachna/logs/crawler/* -mtime +7 -exec rm {} \;
