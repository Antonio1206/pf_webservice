#!/bin/sh

# Make sure only root can run this script
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Install Bash on FreeBSD
pkg install -y bash

# Install lsof on FreeBSD
pkg install -y lsof

# Install python on FreeBSD
pkg install -y python

# Install pip on FreeBSD
pkg install -y py27-pip

# Install pip requirements
pip install -r pf_webservice/source/requirements.txt

# Load pf kernel module
kldload pf 

# Enable PF
pfctl -e 

# Set initial config for PF
echo "pass all no state" > /etc/pf.conf
echo "anchor osmrules" >> /etc/pf.conf
pfctl -f /etc/pf.conf

#Enable forwarding on FreeBSD
sysctl net.inet.ip.forwarding=1
sysctl net.inet6.ip6.forwarding=1

#Disable tcp tso
sysctl net.inet.tcp.tso=0

# Set +x to main.py
chmod +x pf_webservice/source/main.py

# Run main
#nohup pf_webservice/source/main.py > pf.log 2>&1 &
#echo "Web Service Started"
#./pf_webservice/source/main.py &
