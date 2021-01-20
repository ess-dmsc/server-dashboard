#!/bin/bash

# TODO to make this script be more general
# just pass the directory to reference data as argument
# config file should always be named config.json and
# calibration file named calibration.json

efubase=~/deployment/event-formation-unit
cfgdir=/mnt/data/EFU_reference/loki/2021_01/raw

export LD_LIBRARY_PATH=$efubase/lib

BROKER=172.24.0.207:9094
CARBON=172.30.242.21
GRAYLOG=172.30.242.21

config=$cfgdir/config.json
calib=$cfgdir/calib.json

pushd $efubase/bin
  ./efu -d ../modules/loki -p 9021 -m 8021 -f $config --calibration $calib --nohwcheck -b $BROKER -g $CARBON -a $GRAYLOG
popd
