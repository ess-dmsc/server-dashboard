#!/bin/bash

BASE=~/deployment/event-formation-unit

export LD_LIBRARY_PATH=$BASE/lib

BROKER=172.24.0.207:9094
CARBON=172.30.242.21
GRAYLOG=172.30.242.21

pushd $BASE/bin
  ./efu -d ../modules/gdgem --nohwcheck -p 9001 -m 8001 -b $BROKER -g $CARBON -c -5 -f /mnt/data/EFU_reference/gdgem/2018_11/readouts/config.json -a $GRAYLOG
popd
