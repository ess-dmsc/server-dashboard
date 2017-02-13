#!/bin/bash

BANNER=echo
REPOBASE="git@github.com:ess-dmsc/"

function errexit()
{
  echo "Error: $1"
  $BANNER Failed
  exit 1
}

PROJS="event-formation-unit streaming-data-types"

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
  pushd streaming-data-types
    mkdir build
    pushd build
      cmake .. || errexit "cmake failed for streaming-data-types"
      make || errexit "make failed for streaming-data-types"
      cp schemas/*.h $IDIR || errexit "cant copy schema header files"
    popd
  popd
}

function build_efu()
{
  pushd event-formation-unit/prototype2
    make || errexit "make failed for streaming-data-types"
    cp *.so $ODIR || errexit "cant copy loadble instrument pipelines"
    cp efu2 $ODIR || errexit "cant copy event formation exesutable"
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
build_efu

$BANNER Done
