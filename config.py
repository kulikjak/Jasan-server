"""Configuration file for Jasan file server application"""

from os import getenv

APP_NAME = 'Jasan File server'

SERVER_PORT = int(getenv('JASAN_PORT', 5000))
