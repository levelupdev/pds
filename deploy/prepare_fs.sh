#!/bin/bash

# Prepare filesystem (mkdir), install virtualenv

BRANCH_ROOT="../../"
USER_NAME=$USER

make_dirs(){
    (
        cd $BRANCH_ROOT
        echo -n "Creating folders..."
        mkdir -p \
                static \
            && echo "  ok" \
            || echo "  ERROR!" 1>&2;
    )
}

if [ "$1" ]; then
    make_dirs;
    echo "Creating virtual python environment..."
    ./env_update.sh "$1" \
        && echo "  ok" \
        || echo "  ERROR!" 1>&2;
    cd "$BRANCH_ROOT";
    echo "from default_local_settings import *" > local_settings.py
else
   echo "Error: python version requires as first argument" 1>&2;
fi
