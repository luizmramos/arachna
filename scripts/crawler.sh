#!/bin/bash
/usr/bin/python /Arachna/crawler/crawler.py &> /Arachna/logs/crawler/`date +%Y%m%d%H`.log
find /Arachna/logs/crawler/* -mtime +7 -exec rm {} \;
