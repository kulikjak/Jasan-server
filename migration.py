#!./__venv__/bin/python3.6

import time
import random
import logging

from flask import Flask
from pymongo import MongoClient
from urllib.parse import urlsplit

from bson import ObjectId
from model import Model

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_pyfile('config.py')

parsed = urlsplit(app.config['MONGODB_URI'])
mongo_client = MongoClient(app.config['MONGODB_URI'])
db = mongo_client[parsed.path[1:]]

model = Model(db=db)


def add_scream_popularity():
    collection = db['screams']
    screams = collection.find()

    for scream in screams:
        if 'popularity' in scream:
            continue

        scream['popularity'] = 0
        collection.update_one({'_id': scream['_id']}, {'$set': scream})


def add_scream_image():
    collection = db['screams']
    screams = collection.find()

    for scream in screams:
        if 'image' in scream:
            continue

        scream['image'] = None
        collection.update_one({'_id': scream['_id']}, {'$set': scream})


add_scream_popularity()
add_scream_image()
