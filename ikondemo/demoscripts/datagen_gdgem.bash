#!/bin/bash

throttle=${1:-10}

BASE=~/deployment/event-formation-unit

export LD_LIBRARY_PATH=$BASE/lib

while [[ 1 ]]
do
  for filename in ~/ikondata/gdgem/a10000
  do
    $BASE/bin/nmxgen_hits -f $filename -p 9001 -i 172.24.0.205 -t $throttle
    sleep 5
  done
done
