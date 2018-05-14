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
pip install -r requirements.txt

# Load pf kernel module
kldload pf 

# Enable PF
pfctl -e 

# Set +x to main.py
chmod +x main.py

# Run main.py
./main.py
