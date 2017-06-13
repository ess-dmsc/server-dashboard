#!/bin/bash

BANNER=echo
REPOBASE="http://github.com/ess-dmsc/"

########################################################################################
function errexit()
{
  echo "Error: $1"
  $BANNER Failed
  exit 1
}

########################################################################################
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

########################################################################################
function build_data_types()
{
  echo "Building streaming-data-types"
  pushd streaming-data-types/build
    cmake ..             || errexit "cmake failed for streaming-data-types"
    make                 || errexit "make failed for streaming-data-types"
    cp schemas/*.h $IDIR || errexit "cant copy schema header files"
  popd
}

function build_efu()
{
  BSTR_NAME=$(whoami)
  BSTR_DATE=$(date +%F-%H%M%S)
  BSTR_NODE=$(uname -n)
  BSTR_OS=$(uname -r)
  BSTR_HASH=$(git log --oneline | head -n 1 | awk '{print $$1}')
  BUILDSTR=$BSTR_DATE[$BSTR_NODE:$BSTR_NAME][$BSTR_OS]$BSTR_HASH

  echo "Building event-formation-unit"
  pushd event-formation-unit/build
    cmake -DEXTSCHEMAS=ON -DCMAKE_BUILD_TYPE=Release -DBUILDSTR=$BUILDSTR -DCMAKE_INSTALL_PREFIX="" ..
    make install VERBOSE=y  DESTDIR=$BASEDIR/output || errexit "make failed for EFU"
  popd
}

########################################################################################
function build_h5cc()
{
  echo "Building h5cc"
  pushd h5cc/build
    cmake ../source -DCMAKE_INSTALL_PREFIX=""     || errexit "cmake failed"
    make  install DESTDIR=$BASEDIR/output         || errexit "make failed"
  popd
}

########################################################################################
function build_graylog_logger()
{
  echo "Building graylog-logger"
  pushd graylog-logger/graylog_logger/build
    cmake ../.. -DCMAKE_INSTALL_PREFIX=""      || errexit "cmake failed"
    make install DESTDIR=$BASEDIR/output       || errexit "make failed"
  popd
}

########################################################################################
function make_directories()
{
  echo "creating output directories"
  DIRS="$IDIR $ODIR $LDIR $DDIR $UDIR event-formation-unit/build graylog-logger/graylog_logger/build h5cc/build streaming-data-types/build"
  for d in $DIRS
  do
    echo "--$d"
    test -d $d   && errexit "output directory $d already exists"
    mkdir -p $d  || errexit "unable to create directory $d"
  done
}

########################################################################################
function copy_utilities()
{
  echo "Copying utilities"
  pushd event-formation-unit/utils
    cp -r efushell $UDIR     || errexit "couldnt copy efushell to util"
  popd

  echo "Copying scripts"
  pushd event-formation-unit/monitors
    cp -r * $UDIR || errexit "couldnt copy monitor scripts to util"
  popd

  echo "Copying data files"
  pushd event-formation-unit/prototype2
    cp multigrid/calib_data/* $DDIR          || errexit "cant copy data files"
  popd
}

########################################################################################
function make_tar()
{
    tar czvf output.tar.gz output
}

#
# Main script starts here
#
BASEDIR=$(pwd)
git status &>/dev/null && errexit "will not build within git repository please call from other directory"

clone_projects

# Generate line count metrics
cloc --by-file --xml --out=cloc.xml .

IDIR=$BASEDIR/output/include
ODIR=$BASEDIR/output/bin
DDIR=$BASEDIR/output/data
LDIR=$BASEDIR/output/lib
UDIR=$BASEDIR/output/util
make_directories

build_data_types
build_h5cc
build_graylog_logger
build_efu

copy_utilities
make_tar

$BANNER Done
