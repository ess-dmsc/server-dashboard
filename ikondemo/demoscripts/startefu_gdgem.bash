#!/bin/bash

BASE=~/deployment/event-formation-unit

export LD_LIBRARY_PATH=$BASE/lib

BROKER=10.4.0.217:9092
CARBON=10.4.0.216

pushd $BASE/bin
  ./efu -d ../modules/gdgem -p 9001 -m 8001 -b $BROKER -g $CARBON -c -5 -f ~/integration-test/ikondemo/demoscripts/nmx_config.json
popd
