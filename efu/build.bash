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

########################################################################################
function build_efu()
{
  COPYFILES="cspec.so cspec2.so nmx.so udp.so gencspec gencspecfile gennmxfile efu2"

  echo "Building event-formation-unit"
  pushd event-formation-unit/prototype2
    make RELEASE=y HDF5=y GRAYLOG=y EXTSCHEMAS=y V=y  \
         BUILDSTR=integration_test \ # FIXME: set BUILDSTR to something meaningful
         KAFKAINC=$KAFKAINC KAFKALIB=$KAFKALIB        \
         HDF5INC=$HDF5INC   HDF5LIB=$HDF5LIB         || errexit "make failed for EFU"
    for cpfile in $COPYFILES
    do
      echo "Copying "$cpfile
      cp $cpfile $ODIR                               || errexit "cant copy $cpfile to output dir"
    done
  popd
}

########################################################################################
function build_h5cc()
{
  echo "Building h5cc"
  pushd h5cc/build
    cmake ../source || errexit "cmake failed"
    make            || errexit "make failed"
    cp lib* $LDIR   || errexit "cant copy library files"
  popd
}

########################################################################################
function build_graylog_logger()
{
  echo "Building graylog-logger"
  pushd graylog-logger/graylog_logger/build
    cmake ..      || errexit "cmake failed"
    make          || errexit "make failed"
    cp lib* $LDIR || errexit "cant copy library files"
  popd
}

########################################################################################
function make_directories()
{
  echo "creating output directories"
  DIRS='output/bin output/data output/inc output/lib output/util graylog-logger/graylog_logger/build h5cc/build streaming-data-types/build'
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
  pushd event-formation-unit/dataformats/multigrid/scripts
    # cp multigridmon.py $UDIR || errexit "couldnt copy multigrid monitor to util"
    # cp nmxmon.py $UDIR       || errexit "couldnt copy nmx monitor to util"
  popd

  echo "Copying data files"
  pushd event-formation-unit/prototype2
    cp data/* $DDIR          || errexit "cant copy data files"
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

DEFPATH="/opt/dm_group/usr"
KAFKAINC=${1:-$DEFPATH/include}
KAFKALIB=${2:-$DEFPATH/lib}
HDF5INC=${3:-$DEFPATH/include}
HDF5LIB=${4:-$DEFPATH/lib}

echo "KAFKAINC: $KAFKAINC"
echo "KAFKALIB: $KAFKALIB"
echo "HDF5INC: $HDF5INC"
echo "HDF5LIB: $HDF5LIB"

test -d $KAFKAINC || errexit "KAFKAINC: $KAFKAINC does not exist"
test -d $KAFKALIB || errexit "KAFKALIB: $KAFKALIB does not exist"
test -d $HDF5INC  || errexit "HDF5INC: $HDF5INC does not exist"
test -d $HDF5LIB  || errexit "HDF5LIB: $HDF5LIB does not exist"

clone_projects

# Generate line count metrics
cloc --by-file --xml --out=cloc.xml .

make_directories
IDIR=$BASEDIR/output/inc
ODIR=$BASEDIR/output/bin
DDIR=$BASEDIR/output/data
LDIR=$BASEDIR/output/lib
UDIR=$BASEDIR/output/util

build_data_types
build_h5cc
build_graylog_logger
build_efu

copy_utilities
make_tar

$BANNER Done
