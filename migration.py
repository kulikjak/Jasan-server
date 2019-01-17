#!./__venv__/bin/python3.6

import time
import random
import logging

from flask import Flask
from pymongo import MongoClient
from urllib.parse import urlsplit

from bson import ObjectId
from server.model import Model

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_pyfile('server/config.py')

parsed = urlsplit(app.config['MONGODB_URI'])
mongo_client = MongoClient(app.config['MONGODB_URI'])
db = mongo_client[parsed.path[1:]]

model = Model(db=db)


def add_user_ids():
    collection = db['screams']
    screams = collection.find()

    for scream in screams:
        if 'user_id' in scream:
            continue

        scream['user_id'] = None
        collection.update_one({'_id': scream['_id']}, {'$set': scream})

    collection = db['feedbacks']
    feedbacks = collection.find()

    for feedback in feedbacks:
        if 'user_id' in feedback:
            continue

        feedback['user_id'] = None
        collection.update_one({'_id': feedback['_id']}, {'$set': feedback})


def rename_scream_image_attachment():
    collection = db['screams']
    screams = collection.find()

    for scream in screams:
        if 'image' in scream:
            scream['attachment'] = scream['image']

            collection.update_one({'_id': scream['_id']}, {'$unset': {'image': ''}})
            collection.update_one({'_id': scream['_id']}, {'$set': scream})


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


add_scream_image()
add_scream_popularity()
rename_scream_image_attachment()
add_user_ids()
