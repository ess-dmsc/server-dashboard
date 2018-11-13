#!/bin/bash

throttle=${1:-10}

BASE=~/deployment/event-formation-unit

export LD_LIBRARY_PATH=$BASE/lib

while [[ 1 ]]
do
  for filename in ~/ikondata/GEM/*.h5
  do
    $BASE/bin/nmxgen_apv -f $filename -p 9001 -i 172.24.0.205 -t $throttle
    sleep 5
  done
done
