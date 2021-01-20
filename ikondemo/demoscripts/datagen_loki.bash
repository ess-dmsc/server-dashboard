#!/bin/bash

throttle=50000

BASE=~/deployment/event-formation-unit

data1=/mnt/data/EFU_reference/loki/2020/wireshark/loki_data_181220.pcapng
data2=/mnt/data/EFU_reference/loki/2021_01/raw/mask.dat

export LD_LIBRARY_PATH=$BASE/lib

while [[ 1 ]]
do
   #$BASE/bin/udpgen_pcap -t $throttle -f $data1  -i 172.24.0.205 -p 9021
   $BASE/bin/udpgen_lokiraw -t $throttle -f $data2  -i 172.24.0.205 -p 9021
done
