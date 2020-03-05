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

config=/mnt/data/EFU_reference/gdgem/2020_02/wireshark/GDDLAB_config.json
calib=/mnt/data/EFU_reference/gdgem/2020_02/wireshark/GDDLAB_calib.json

pushd $BASE/bin
  ./efu -d ../modules/gdgem -r 1 --pmin 0 --pmax 127 --pwidth 64 --nohwcheck -p 9010 -m 8010 -b $BROKER -g $CARBON --file $config --calibration $calib -a $GRAYLOG
popd
