#!/bin/bash

throttle=10

BASE=~/deployment/event-formation-unit

export LD_LIBRARY_PATH=$BASE/lib

while [[ 1 ]]
do
  for filename in ~/ikondata/GEM/*.h5
  do
    $BASE/bin/gennmxfile -f $filename -p 9001 -i 172.24.0.201 -t $throttle
    sleep 5
  done
done
