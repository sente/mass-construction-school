#!/usr/bin/python

import sys
import os

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0,here)

from mare import create_app

application = create_app('mare')
