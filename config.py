"""Configuration file for Jasan file server application"""

from os import getenv

APP_NAME = 'Jasan File server'

SERVER_PORT = int(getenv('JASAN_PORT', 80))
SERVER_ADDRESS = getenv('JASAN_ADDRESS', 'http://localhost:{}/'.format(SERVER_PORT))

FILE_ROOT = getenv('JASAN_FILE_ROOT', 'Jasan')
