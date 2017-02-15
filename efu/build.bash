#!/bin/bash

BANNER=echo
REPOBASE="git@github.com:ess-dmsc/"

function errexit()
{
  echo "Error: $1"
  $BANNER Failed
  exit 1
}

PROJS="event-formation-unit streaming-data-types h5cc graylog-logger"

function clone_projects()
{
  for proj in $PROJS
  do
    echo "Cloning $proj"
    test -d $proj && errexit "directory already exist"
    git clone ${REPOBASE}${proj}.git || errexit "unable to clone $proj"
  done
}

function build_data_types()
{
  echo "Building streaming-data-types"
  mkdir -p streaming-data-types/build || errexit "cant make build dir"
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
    make NOKAFKA=y HDF5=y V=y || errexit "make failed for EFU"
    mkdir -p $ODIR/data || errexit "cant create data dir"
    cp data/* $ODIR/data || errexit "cant copy data files"
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
  mkdir -p h5cc/build || errexit "cant create h5cc build dir"
  pushd h5cc/build
    cmake ../source || "cmake failed for h5cc"
    make || errexit "make failed for h5cc"
  popd
}

function build_graylog_logger()
{
  echo "Building graylog-logger"
  pushd graylog-logger/graylog_logger
    mkdir build
    pushd build
      cmake ..
      make || errexit "make failed for graylog-logger"
    popd
  popd
}


git status &>/dev/null && errexit "will not build within git repository please call from other directory"

test -d include && errexit "include directory already exist"
mkdir include
IDIR=$(pwd)/include

test -d output && errexit "output directory already exist"
mkdir output
ODIR=$(pwd)/output
clone_projects
build_data_types
build_h5cc
build_graylog_logger
build_efu

$BANNER Done
