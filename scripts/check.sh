#!/bin/bash
[ "`service arachna status | grep -c not`" = 1 ] && sudo service arachna start
