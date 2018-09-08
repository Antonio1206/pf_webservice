#!/usr/bin/env python

from flask import Flask, request
from api.v1 import v1
import sys
import re


app = Flask(__name__)
app.register_blueprint(v1)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=9999, threaded=True)
