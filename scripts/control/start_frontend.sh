#!/bin/bash

target=$1

FRONTEND_PATH=$(realpath "vigil/frontend")

if [[ $target == *"prod"* ]]; then
    cd $FRONTEND_PATH && npm start && cd "../../"
else
    cd $FRONTEND_PATH && npm start && cd "../../"
fi

