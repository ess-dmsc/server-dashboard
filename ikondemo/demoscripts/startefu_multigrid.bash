#!/bin/bash

BASE=~/deployment/event-formation-unit

export LD_LIBRARY_PATH=$BASE/lib

BROKER=172.24.0.207:9092
CARBON=10.4.0.216

pushd $BASE/bin
  ./efu -d ../modules/mgcncs2 -p 9000 -m 8000 -b $BROKER -g $CARBON -c -5
popd
