#!/bin/sh

if [ $# -ne 1 ] 
then
    echo "Usage: sh add_rule.sh <rule_to_add>"
    return 1
fi

newrule=$1

cmd="echo \"$newrule\" >> osmconfig"
eval $cmd

if [ $? -ne 0 ]
then
    return $?
fi

cmd="sudo pfctl -a osmrules -f osmconfig"
eval $cmd
if [ $? -ne 0 ]
then
    return $?
fi

