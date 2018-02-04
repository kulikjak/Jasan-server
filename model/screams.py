import pymongo
import datetime

from bson import ObjectId


class Screams(object):

    COLLECTION_NAME = 'screams'

    def __init__(self, model, db):
        self._model = model
        self._db = db
        self._collection = db[self.COLLECTION_NAME]

    def create_scream(self, data):
        scream = Scream({
            '_id': ObjectId(),
            'created': datetime.datetime.utcnow(),
            'name': data['name'],
            'text': data['text']
        })
        self._collection.insert_one(scream.serialize())

        return scream

    def save(self, scream):
        self._collection.update_one({'_id': scream._id}, {'$set': scream.serialize(update=True)})

    def delete(self, scream):
        self._collection.delete_one({'_id': scream._id})

    def find(self):
        doc = self._collection.find({}).sort('created', pymongo.DESCENDING)

        screams = []
        for scream in doc:
            screams.append(Scream(scream))

        return screams


class Scream(object):

    def __init__(self, scream):
        self._id = scream['_id']
        self._created = scream['created']
        self._name = scream['name']
        self._text = scream['text']

    def serialize(self, update=False):
        scream = {'name': self._name, 'text': self._text}

        if not update:
            scream['_id'] = self._id
            scream['created'] = self._created

        return scream

    def get_serialized_data(self):
        return {
            'id': str(self._id),
            'created': self._created.isoformat(),
            'name': self._name,
            'text': self._text
        }

    def get_id(self):
        return str(self._id)

    def get_name(self):
        return self._name

    def get_text(self):
        return self._text

    def get_created(self):
        return self._created.isoformat()

    def __repr__(self):
        return '<{!r} id={!r} name={!r} text={!r}>' \
            .format(self.__class__.__name__, self._id, self._name, self._text)
