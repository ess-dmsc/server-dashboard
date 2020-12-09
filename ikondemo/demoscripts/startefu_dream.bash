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

config=/mnt/data/EFU_reference/jalousie/2019_07/v20_mappings.json


pushd $BASE/bin
  ./efu -d ../modules/jalousie -p 9031 -m 8031 -f $config --nohwcheck -b $BROKER -g $CARBON -a $GRAYLOG
popd
