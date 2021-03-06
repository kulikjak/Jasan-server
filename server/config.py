"""Configuration file for Jasan server application"""

from os import getenv

VERSION = '0.1'
APP_NAME = 'Jasan File server'

SERVER_PORT = int(getenv('JASAN_PORT', 8000))
SERVER_ADDRESS = getenv('JASAN_SERVER_ADDRESS', 'http://jasan.lan/')

SECRET_KEY = getenv('JASAN_SECRET_KEY', 'S3cr3tK3y')
MONGODB_URI = getenv('JASAN_MONGODB_URI', 'mongodb://localhost:27017/jasan')

JOURNAL_ROOT = 'journal'
UPLOAD_FOLDER = 'uploads'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
