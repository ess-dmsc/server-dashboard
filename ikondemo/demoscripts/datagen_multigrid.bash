#!/bin/bash

throttle=$1

BASE=/home/mortenchristensen/output

export LD_LIBRARY_PATH=/opt/dm_group/usr/lib:$BASE/lib


$BASE/util/efushell/mgloadcal.py -i 10.4.0.215 -p 8000 /home/mortenchristensen/ikondemo/cncs_10_13

while [[ 1  ]]
do 
   $BASE/bin/mgcncsgenfile -f ../detectordata/cncs_10_13.bin -t $throttle -i 172.24.0.201 -p 9000
   sleep 5
done
