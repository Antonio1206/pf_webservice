#!/bin/sh

if [ $# -ne 0 ]
then
    echo "Usage: sh flush_rules.sh"
    return 1
fi

sudo pfctl -a osmconfig -F rules

if [ $? -ne 0 ]
then
    return $?
fi
