#!/usr/bin/env python

import sys
import os
import re
import subprocess

class Fatal(Exception):
    pass

def pfctl(args, stdin=None):
    argv = ['pfctl'] + list(args.split(" "))
    print argv
    return 0
    p = subprocess.Popen(argv, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    o = p.communicate(stdin)
    if p.returncode:
        print Fatal('%r returned %d' % (argv, p.returncode))
    return o

def PFenable():
    pfctl("-e")

def PFdisable():
    pfctl("-d")

#def exec_sh(args, stdin=None):
#    argv = ['sh'] + list(args.split(" "))
#
#    p = subprocess.Popen(argv, stdin=subprocess.PIPE,
#                         stdout=subprocess.PIPE,
#                         stderr=subprocess.PIPE)
#    o = p.communicate(stdin)
#    if p.returncode:
#        print Fatal('%r returned %d' % (argv, p.returncode))
#    return o
