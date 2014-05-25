#!/bin/bash
wget --spider -T 5 -t 2 "http://localhost:80/" &> /dev/null || (sudo service arachna restart && date "+%Y-%m-%d %H:%M" >> /Arachna/logs/server/down.log)
