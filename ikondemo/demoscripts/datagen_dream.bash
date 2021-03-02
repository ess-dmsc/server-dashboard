#!/bin/bash

throttle=1000

base=~/deployment/event-formation-unit
datadir=/mnt/data/EFU_reference/jalousie
datafile1=$datadir/2019_07/noise.bin
datafile2=$datadir/2021/simulation/data_no_dup.txt
datafile3=$datadir/2021/simulation/data_dream_mask1.txt
datafile4=$datadir/2021/simulation/data_dream_mask2.txt
ipparms="-i 172.24.0.205 -p 9031"

export LD_LIBRARY_PATH=$BASE/lib

while [[ 1 ]]
do
   $base/bin/udpgen_jalousie -f $datafile1 $ipparms -t $throttle
   sleep 5
   $base/bin/udpgen_dreamsim -f $datafile2 $ipparms -t $throttle
   sleep 5
   $base/bin/udpgen_dreamsim -f $datafile3 $ipparms -t $throttle
   sleep 5
   $base/bin/udpgen_dreamsim -f $datafile4 $ipparms -t $throttle
   sleep 5
done
