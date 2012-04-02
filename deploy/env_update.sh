#!/bin/bash
# Removes old virtualenv, install new one

ENV_PATH='../../env';

if [ $1 ]; then
    rm -r "$ENV_PATH";
    virtualenv --python="python$1" "$ENV_PATH";
    source "$ENV_PATH/bin/activate";
    pip install -r virtualenv.req --use-mirrors;
else
   echo "Error: python version requires as first argument" 1>&2;
fi
