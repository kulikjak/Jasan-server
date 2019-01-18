import logging
import os
import urllib

import flask
import flask_login
import pymongo

from server.model import Model
from server.util import check_config
from server.util import setup_logging

# create logger
logger = logging.getLogger(__name__)
setup_logging()

# create Flask application
app = flask.Flask(__name__)
app.config.from_pyfile('config.py')

check_config(app)

# prepare database connection
parsed = urllib.parse.urlsplit(app.config['MONGODB_URI'])
mongo_client = pymongo.MongoClient(app.config['MONGODB_URI'])
db = mongo_client[parsed.path[1:]]

# init model of the application
model = Model(db=db)


@app.before_request
def before_request():
    flask.g.model = model

from server import controller
