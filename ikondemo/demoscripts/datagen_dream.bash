#!/bin/bash

throttle=1000

base=~/deployment/event-formation-unit
datadir=/mnt/data/EFU_reference/jalousie

datafile1=$datadir/2021/simulation/data_no_dup.txt
datafile2=$datadir/2021/simulation/data_dream_mask1.txt
datafile3=$datadir/2021/simulation/data_dream_mask2.txt

ipparms="-i 172.24.0.203 -p 9031"

export LD_LIBRARY_PATH=$base/lib

while [[ 1 ]]
do
   $base/bin/udpgen_dreamsim -f $datafile1 $ipparms -t $throttle
   sleep 10
   $base/bin/udpgen_dreamsim -f $datafile2 $ipparms -t $throttle
   sleep 10
   $base/bin/udpgen_dreamsim -f $datafile3 $ipparms -t $throttle
   sleep 10
done
