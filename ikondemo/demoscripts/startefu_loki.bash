#!/bin/bash

# TODO to make this script be more general
# just pass the directory to reference data as argument
# config file should always be named config.json and
# calibration file named calibration.json

BASE=~/deployment/event-formation-unit

export LD_LIBRARY_PATH=$BASE/lib

BROKER=172.24.0.207:9094
CARBON=172.30.242.21
GRAYLOG=172.30.242.21

config=/mnt/data/EFU_reference/loki/2020/wireshark/config.json


pushd $BASE/bin
  ./efu -d ../modules/loki --nohwcheck -p 9021 -m 8021 -b $BROKER -g $CARBON --file $config --calibration $calib -a $GRAYLOG
popd
