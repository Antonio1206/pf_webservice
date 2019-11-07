#!/usr/bin/env python2

from flask import Flask, request
from api.v1 import v1
import sys
import re


app = Flask(__name__)
app.register_blueprint(v1)

if __name__ == '__main__':
    port = 9999
    if len(sys.argv) == 2:
        try:
            port = int(sys.argv[1])
        except:
            port = 9999
    app.run(host='0.0.0.0', port=port, threaded=True)
