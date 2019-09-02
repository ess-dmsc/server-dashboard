#!/bin/bash

BASE=~/deployment/event-formation-unit

export LD_LIBRARY_PATH=$BASE/lib

BROKER=172.24.0.207:9094
CARBON=172.30.242.21
GRAYLOG=172.30.242.21

pushd $BASE/bin
  ./efu -d ../modules/mgmesytec -f /mnt/data/EFU_reference/multigrid/2018_09_03/Sequoia_mappings2.json --nohwcheck -p 9000 -m 8000 -b $BROKER -g $CARBON -a $GRAYLOG
popd
