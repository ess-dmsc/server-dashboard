#!/bin/bash

throttle=100000

BASE=~/deployment/event-formation-unit

export LD_LIBRARY_PATH=$BASE/lib

while [[ 1 ]]
do
   $BASE/bin/udpgen_pcap -t $throttle -f /mnt/data/EFU_reference/multiblade/2018_11_22/wireshark/ess2_ess_mask.pcap -i 172.24.0.205 -p 9003
done
