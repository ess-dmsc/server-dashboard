#!/bin/bash

throttle=1000

BASE=~/deployment/event-formation-unit

data1=/mnt/data/EFU_reference/loki/2021_05/mjc_test_II.pcap

export LD_LIBRARY_PATH=$BASE/lib

while [[ 1 ]]
do
   $BASE/bin/udpgen_pcap -t $throttle -f $data1  -i 172.24.0.221 -p 9021
done
