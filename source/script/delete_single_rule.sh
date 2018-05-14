#!/bin/sh

if [ $# -ne 1 ]
then
    echo "Usage: sh delete_single_rule.sh <line_number>"
    return 1
fi

line_number=$1
sed_operation=d

case $1 in
  *[!0-9]* | '') echo Not a number; return 1 ;;
esac

if [ ! -f osmconfig ]
then
   echo "" > osmconfig
fi

cmd="mv osmconfig tmposmconfig"
eval $cmd
if [ $? -ne 0 ]
then
    return $?
fi

cmd="sed -e '$line_number$sed_operation' tmposmconfig > osmconfig"
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

rm tmposmconfig
