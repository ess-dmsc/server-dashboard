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
  ./efu -d ../modules/gdgem -p 9011 -m 8011 -f $config --calibration $calib -r 2 --pmin 64 --pmax 128 --pwidth 32 --nohwcheck -b $BROKER -g $CARBON -a $GRAYLOG
popd
