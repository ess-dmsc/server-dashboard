#!/bin/bash

ofile=/tmp/ikondemoethstats

while [[ 1 ]]
do
  date=$(date +%s)
  /usr/sbin/ethtool -S ens1 > $ofile

  rx_packets=$(grep rx_packets:  $ofile | awk -e '{print $2}')
  rx_bytes=$(grep rx_bytes: $ofile | awk -e '{print $2}')
  rx_packets_phy=$(grep rx_packets_phy $ofile | awk -e '{print $2}')
  rx_bytes_phy=$(grep rx_bytes_phy $ofile | awk -e '{print $2}')

  echo "efu2.100g.rx_bytes ${rx_bytes} $date"
  echo "efu2.100g.rx_packets ${rx_packets} $date"
  echo "efu2.100g.rx_bytes_phy ${rx_bytes_phy} $date"
  echo "efu2.100g.rx_packets_phy ${rx_packets_phy} $date"

  echo "efu2.100g.rx_bytes ${rx_bytes} $date" | nc 10.4.0.216 2003
  echo "efu2.100g.rx_packets ${rx_packets} $date" | nc 10.4.0.216 2003
  echo "efu2.100g.rx_bytes_phy ${rx_bytes_phy} $date" | nc 10.4.0.216 2003
  echo "efu2.100g.rx_packets_phy ${rx_packets_phy} $date" | nc 10.4.0.216 2003
  rm -f $ofile
  sleep 0.98
done
