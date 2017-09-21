#!/bin/bash

BASE=/home/mortenchristensen

export LD_LIBRARY_PATH=/opt/dm_group/usr/lib:$BASE/output/lib

BROKER=172.24.0.205:9092
CARBON=10.4.0.216

pushd $BASE/output/bin
pwd
./efu2 -d mgcncs2 -p 9000 -m 8000 -b $BROKER -g $CARBON -c -5
popd
