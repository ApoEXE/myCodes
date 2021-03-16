#! /usr/bin/python3

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/jav/myCodes/plotting/')
from app import app as application
application.secret_key = 'abcd'
