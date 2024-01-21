#!/bin/bash

WEB_RUN_DIR="${1}"  # run dir, create and input by python script
WINMUT_MAX_RUN_CASES="${2}"

WEB_RUN_DIR_SRC="${WEB_RUN_DIR}/src"
WEB_RUN_DIR_BIN="${WEB_RUN_DIR}/bin"
WEB_RUN_DIR_LOG="${WEB_RUN_DIR}/log"

mkdir ${WEB_RUN_DIR_SRC}
mkdir ${WEB_RUN_DIR_BIN}
mkdir ${WEB_RUN_DIR_LOG}

# copy source code
RAW_SCR_DIR="demo/src"
cp -r ${RAW_SCR_DIR}/* ${WEB_RUN_DIR_SRC}

# complier dir
WINMUT_BASE_DIR="$(pwd)/../../../../cmake-build-release/"

export CFLAGS="-accmut -winmut-no-opt -O2 ${CFLAGS}"   # AccMut algorithm
# export CFLAGS="-winmut -O2 ${CFLAGS}"   # WinMut algorithm

export CC="${WINMUT_BASE_DIR}/bin/clang ${CFLAGS}"
export CXX="${WINMUT_BASE_DIR}/bin/clang++"
export LD_PRELOAD="${WINMUT_BASE_DIR}/lib/libLLVMWinMutRuntime.so"

cd ${WEB_RUN_DIR}

# build
export WINMUT_DISABLED=YES
make

# run
export WINMUT_DISABLED=NO
export WINMUT_LOG_FILE_PREFIX=${WEB_RUN_DIR_LOG}
export WINMUT_MAX_RUN_CASES          # HAVE TO DEFINE THIS TO MAKE TOOL OUTPUT WORK!!!

make test