#!/bin/sh

for var in $@
do
echo ifconfig_$var=\"DHCP\" >> rc.conf
done

for var in $@
do
ifconfig $var down
ifconfig $var up
done

