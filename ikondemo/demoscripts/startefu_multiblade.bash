#!/bin/bash

BASE=~/deployment/event-formation-unit

export LD_LIBRARY_PATH=$BASE/lib

BROKER=172.24.0.207:9092
CARBON=10.4.0.216

pushd $BASE/bin
  ./efu -d ../modules/mbcaen -f ~/integration-test/ikondemo/demoscripts/multiblade_config.json --nohwcheck -p 9003 -m 8003 -b $BROKER -g $CARBON
popd
