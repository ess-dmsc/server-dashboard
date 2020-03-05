#!/bin/bash

throttle=${1:-10}

BASE=~/deployment/event-formation-unit

export LD_LIBRARY_PATH=$BASE/lib

while [[ 1 ]]
do
  $BASE/bin/udpgen_pcap -f /mnt/data/EFU_reference/gdgem/2020_02/wireshark/bat.pcapng -p 9010 -i 172.24.0.205 -t $throttle
  $BASE/bin/udpgen_pcap -f /mnt/data/EFU_reference/gdgem/2020_02/wireshark/bat.pcapng -p 9011 -i 172.24.0.205 -t $throttle
  sleep 5
done
