#!/bin/bash

BANNER=echo
REPOBASE="http://github.com/ess-dmsc/"

function errexit()
{
  echo "Error: $1"
  $BANNER Failed
  exit 1
}

function clone_projects()
{
  echo "Cloning projects: "
  PROJS="event-formation-unit streaming-data-types h5cc graylog-logger"
  for proj in $PROJS
  do
    echo "-- $proj"
    test -d $proj && errexit "directory already exist"
    git clone ${REPOBASE}${proj}.git || errexit "unable to clone $proj"
  done
}

function build_data_types()
{
  echo "Building streaming-data-types"
  pushd streaming-data-types/build
    cmake .. || errexit "cmake failed for streaming-data-types"
    make || errexit "make failed for streaming-data-types"
    cp schemas/*.h $IDIR || errexit "cant copy schema header files"
  popd
}

function build_efu()
{
  COPYFILES="cspec.so cspec2.so nmx.so udp.so gencspec gencspecfile gennmxfile efu2"

  echo "Building event-formation-unit"
  echo "NOKAFKA!"
  pushd event-formation-unit/prototype2
    make NOKAFKA=y HDF5=y GRAYLOG=y V=y || errexit "make failed for EFU"
    cp data/* $DDIR || errexit "cant copy data files"
    for cpfile in $COPYFILES
    do
      echo "Copying "$cpfile
      cp $cpfile $ODIR || errexit "cant copy $cpfile to output dir"
    done
  popd
}

function build_h5cc()
{
  echo "Building h5cc"
  pushd h5cc/build
    cmake ../source || "cmake failed for h5cc"
    make || errexit "make failed for h5cc"
    cp lib* $LDIR || errexit "cant copy library files"
  popd
}

function build_graylog_logger()
{
  echo "Building graylog-logger"
  pushd graylog-logger/graylog_logger/build
    cmake ..
    make || errexit "make failed for graylog-logger"
    cp lib* $LDIR ||errexit "cant copy library files"
  popd
}

function make_directories()
{
  echo "creating output directories"
  DIRS='output/bin output/data output/inc output/lib output/util graylog-logger/graylog_logger/build h5cc/build streaming-data-types/build'
  for d in $DIRS
  do
    echo "--$d"
    test -d $d && errexit "output directory $d already exists"
    mkdir -p $d || errexit "unable to create directory $d"
  done
}

function copy_utilities()
{
  echo "Copying utilities"
  pushd event-formation-unit/utils
    cp -r efushell $UDIR  || errexit "couldnt copy efushell to util"
  popd
  pushd event-formation-unit/dataformats/cncs2016/scripts
    cp multigridmon.py $UDIR || echo "couldnt copy multigrid monitor to util"
    cp nmxmon.py $UDIR || echo "couldnt copy nmx monitor to util"
  popd
}

git status &>/dev/null && errexit "will not build within git repository please call from other directory"

clone_projects

make_directories
IDIR=$(pwd)/output/inc
ODIR=$(pwd)/output/bin
DDIR=$(pwd)/output/data
LDIR=$(pwd)/output/lib
UDIR=$(pwd)/output/util

build_data_types
build_h5cc
build_graylog_logger
build_efu

copy_utilities

$BANNER Done
