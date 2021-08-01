#!/usr/bin/env bash

SCRIPT_DIR=$( cd ${0%/*} && pwd -P )
ROOT_DIR=$( cd "$SCRIPT_DIR/../.." && pwd -P )
cd $ROOT_DIR
if [[ ! -d "datum" ]]; then
    echo "ERROR: PWD: $PWD is not project root"
    exit 1
fi

set -x

PLATFORM="$(uname -s | tr 'A-Z' 'a-z')"

if [[ ${PLATFORM} == "darwin" ]]; then
    N_JOBS=$(sysctl -n hw.ncpu)
else
    N_JOBS=$(grep -c ^processor /proc/cpuinfo)
fi


echo ""
echo "Pytest will use ${N_JOBS} concurrent job(s)."
echo ""

export CC_OPT_FLAGS='-mavx'
export TF_NEED_CUDA=0

export PYTHON_PATH=$PWD
pytest -v -rs --cov-report term-missing --cov=datum --durations=10 -n ${N_JOBS} tests/
exit $?
