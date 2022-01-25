#!/bin/bash

throttle=${1:-10}

BASE=~/deployment/event-formation-unit

export LD_LIBRARY_PATH=$BASE/lib


function loadandrun()
{
  $BASE/bin/udpgen_vmm3_let -i 172.24.0.221 -t $throttle -p 9001
}


while [[ 1 ]]
do
   loadandrun
done
