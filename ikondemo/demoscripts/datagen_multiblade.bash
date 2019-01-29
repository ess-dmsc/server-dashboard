#!/bin/bash

throttle=${1:-100}

BASE=~/deployment/event-formation-unit

export LD_LIBRARY_PATH=$BASE/lib

while [[ 1 ]]
do
   $BASE/bin/udpgen_pcap -t $throttle -f ~/ikondata/multiblade/ess2_ess_mask.pcap -i 172.24.0.205 -p 9003
done
