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

#config=/mnt/data/EFU_reference/gdgem/2018_11/readouts/config.json
#calib=
config=/mnt/data/EFU_reference/gdgem/2019_09/readouts/config.json
calib=/mnt/data/EFU_reference/gdgem/2019_09/readouts/Budapest_time_calib_BC_20MHz_TAC_100ns.json


pushd $BASE/bin
  ./efu -d ../modules/gdgem -p 9001 -m 8001 -f $config --calibration $calib --nohwcheck -b $BROKER -g $CARBON -a $GRAYLOG
popd
