#!/bin/bash

BASE=~/deployment/event-formation-unit

export LD_LIBRARY_PATH=$BASE/lib

BROKER=172.24.0.205:9092
CARBON=10.4.0.216

pushd $BASE/bin
  ./efu -d ../modules/sonde -p 9002 -m 8002 -b $BROKER -g $CARBON -c -5
popd
