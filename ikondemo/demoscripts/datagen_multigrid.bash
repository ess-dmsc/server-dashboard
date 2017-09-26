#!/bin/bash

throttle=${1:-10}

BASE=~/output

export LD_LIBRARY_PATH=/opt/dm_group/usr/lib:$BASE/lib


function loadandrun()
{
  CALIB=$1
  RUN=$2
  $BASE/util/efushell/mgloadcal.py -i 10.4.0.215 -p 8000 $CALIB
  $BASE/bin/mgcncsgenjson -b ~/ikondata/MG_CNCS -r ~/dmg-build-scripts/ikondemo/demoscripts/allfiles.json -j $RUN -t $throttle -i 172.24.0.201 -p 9000
}



while [[ 1  ]]
do
   loadandrun ~/dmg-build-scripts/ikondemo/demoscripts/mgcalib/validruns_15 ikon1
   loadandrun ~/dmg-build-scripts/ikondemo/demoscripts/mgcalib/validruns_13 ikon2
   loadandrun ~/dmg-build-scripts/ikondemo/demoscripts/mgcalib/validruns_19 ikon1
   loadandrun ~/dmg-build-scripts/ikondemo/demoscripts/mgcalib/validruns_10 ikon3
done
