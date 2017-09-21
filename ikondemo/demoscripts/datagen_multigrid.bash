#!/bin/bash

throttle=$1

BASE=~/output

export LD_LIBRARY_PATH=/opt/dm_group/usr/lib:$BASE/lib


function loadandrun()
{
  CALIB=$1
  RUN=$2
  $BASE/util/efushell/mgloadcal.py -i 10.4.0.215 -p 8000 $CALIB
  #$BASE/bin/mgcncsgenfile -f ../detectordata/cncs_10_13.bin -t $throttle -i 172.24.0.201 -p 9000
  $BASE/bin/mgcncsgenjson -b ~/detectordata -r allfiles.json -j ikon1 -t $throttle -i 172.24.0.201 -p 9000
}



while [[ 1  ]]
do
   loadandrun ~/dmg-build-scripts/ikondemo/demoscripts/mgcalib/validruns_15 ikon1
   loadandrun ~/dmg-build-scripts/ikondemo/demoscripts/mgcalib/validruns_15 ikon2
done
