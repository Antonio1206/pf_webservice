#!/bin/sh

# Make sure only root can run our script
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

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
echo "pass all" > /etc/pf.conf
echo "anchor osmrules" >> /etc/pf.conf
pfctl -f /etc/pf.conf

# Set +x to main.py
chmod +x pf_webservice/source/main.py

# Run main.py
./pf_webservice/source/main.py
