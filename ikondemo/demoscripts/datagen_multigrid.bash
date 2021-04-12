#!/bin/bash

throttle=${1:-10}

BASE=~/deployment/event-formation-unit

export LD_LIBRARY_PATH=$BASE/lib


function loadandrun()
{
  $BASE/bin/mggen_readouts -f /mnt/data/EFU_reference/multigrid/2018_09_03/readouts/154484 -i 172.24.0.221 -t $throttle -p 9000 -b 4500
}


while [[ 1 ]]
do
   loadandrun
done
