#!/bin/sh

for var in $@
do
echo ifconfig_$var=\"DHCP -rxcsum -txcsum\" | tee -a /etc/rc.conf > /dev/null
done

for var in $@
do
ifconfig $var down
ifconfig $var up
ifconfig $var -rxcsum -txcsum
done

exit 0

