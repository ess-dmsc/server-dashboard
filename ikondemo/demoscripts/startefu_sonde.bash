#!/bin/bash

BASE=~/deployment/event-formation-unit

export LD_LIBRARY_PATH=$BASE/lib

BROKER=172.24.0.207:9092
CARBON=172.30.242.21

pushd $BASE/bin
  ./efu -d ../modules/sonde --min_mtu 1500 -p 9002 -m 8002 -b $BROKER -g $CARBON -c -5
popd
