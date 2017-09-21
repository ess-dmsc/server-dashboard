#!/bin/bash

BASE=/home/mortenchristensen/output

export LD_LIBRARY_PATH=/opt/dm_group/usr/lib:$BASE/lib

while [[ 1 ]]
do 
   $BASE/bin/gennmxfile -f ../detectordata/GEM_3300V_4000V_2cm_2cm_dataTree_thresh100.h5 -t 10 -i 172.24.0.201 -p 9001
   sleep 5
done
