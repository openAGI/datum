#!/bin/bash

set -vx  # print command from file as well as evaluated command
set -e   # fail and exit on any command erroring

source ./tools/build/utils.sh
function setup_env() {
  create_env
  pip install -q --upgrade setuptools pip
  pip install -q wheel twine pyopenssl
}

GIT_COMMIT_ID=${1:-""}
[[ -z $GIT_COMMIT_ID ]] && echo "Must provide a commit" && exit 1
SETUP_ARGS=""
if [ "$GIT_COMMIT_ID" = "nightly" ]
then
  GIT_COMMIT_ID="master"
  SETUP_ARGS="--nightly"
  export TFDS_NIGHTLY_TIMESTAMP=$(date +"%Y%m%d%H%M")
fi

TMP_DIR=$(mktemp -d)
pushd $TMP_DIR
echo $TMP_DIR

echo "Cloning openagi/datum and checking out commit $GIT_COMMIT_ID"
git clone https://github.com/n3011/datum.git
cd datum

git checkout $GIT_COMMIT_ID

echo "Building source distribution"

# Build the wheels
# setup_env
python setup.py sdist $SETUP_ARGS
python setup.py bdist_wheel $SETUP_ARGS

# Publish to PyPI
read -p "Publish? (y/n) " -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
  echo "Publishing to PyPI"
  twine upload dist/*
else
  echo "Skipping upload"
  exit 1
fi

popd
rm -rf $TMP_DIR
