#!/bin/bash

BASEDIR=$(dirname "$0")
echo "$BASEDIR"

python $BASEDIR/wlt.py "$@"