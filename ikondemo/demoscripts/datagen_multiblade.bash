#!/bin/bash

throttle=50000

BASE=~/deployment/event-formation-unit

export LD_LIBRARY_PATH=$BASE/lib

while [[ 1 ]]
do
   #$BASE/bin/udpgen_pcap -t $throttle -f /mnt/data/EFU_reference/multiblade/2021/08_artificial_pcap/Freia_VMM3a.pcapng -i 172.24.0.221 -p 9003
   $BASE/bin/udpgen_vmm3_freia -l -r 22 -o 400 -t $throttle -i 172.24.0.221 -p 9003
done
