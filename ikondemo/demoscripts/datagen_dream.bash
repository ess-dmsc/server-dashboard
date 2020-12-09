#!/bin/bash

throttle=50000

BASE=~/deployment/event-formation-unit

export LD_LIBRARY_PATH=$BASE/lib

while [[ 1 ]]
do
   $BASE/bin/udpgen_jaloisue -t $throttle -f /mnt/data/EFU_reference/jalousie/2019_07/noise.bin -i 172.24.0.205 -p 9031
done
