#! /usr/bin/python3

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/python/image-processing/')
from image import app as application
application.secret_key = 'anything you wish'
