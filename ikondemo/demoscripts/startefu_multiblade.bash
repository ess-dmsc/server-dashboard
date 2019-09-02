#!/bin/bash

BASE=~/deployment/event-formation-unit

export LD_LIBRARY_PATH=$BASE/lib

BROKER=172.24.0.207:9094
CARBON=172.30.242.21
GRAYLOG=172.30.242.21

pushd $BASE/bin
  ./efu -d ../modules/mbcaen -f ~/integration-test/ikondemo/demoscripts/multiblade_config.json --nohwcheck -p 9003 -m 8003 -b $BROKER -g $CARBON -a $GRAYLOG
popd
