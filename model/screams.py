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
            'text': data['text'],
            'user_id': data['user_id'],
            'attachment': data['attachment'],
            'popularity': None
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

    def find_one(self, scream_id=None):
        query = {}
        if scream_id is not None:
            query['_id'] = ObjectId(scream_id)

        doc = self._collection.find_one(query)
        if not doc:
            return None

        return Scream(doc)


class Scream(object):

    def __init__(self, scream):
        self._id = scream['_id']
        self._created = scream['created']
        self._name = scream['name']
        self._text = scream['text']
        self._user_id = scream['user_id']
        self._attachment = scream['attachment']
        self._popularity = scream['popularity']

    def serialize(self, update=False):
        scream = {
            'name': self._name,
            'text': self._text,
            'user_id': self._user_id,
            'attachment': self._attachment,
            'popularity': self._popularity
        }

        if not update:
            scream['_id'] = self._id
            scream['created'] = self._created

        return scream

    def get_serialized_data(self):
        return {
            'id': str(self._id),
            'created': self._created.isoformat(),
            'name': self._name,
            'text': self._text,
            'attachment': self._attachment,
            'user_id': self._user_id,
            'popularity': self._popularity
        }

    def get_id(self):
        return str(self._id)

    def get_name(self):
        return self._name

    def get_text(self):
        return self._text

    def get_created(self):
        return self._created.isoformat()

    def get_user_id(self):
        return self._user_id

    def get_attachment(self, thumbnail=False):
        if thumbnail:
            path, ext = self._attachment.split('.')
            return '{}_thumbnail.{}'.format(path, ext)
        return self._attachment

    def get_popularity(self):
        return self._popularity if self._popularity else 0

    def increase_popularity(self, amount):
        if self._popularity:
            self._popularity += amount
        else:
            self._popularity = amount

    def set_data(self, data):
        self._name = data['name'] if 'name' in data else self._name
        self._text = data['text'] if 'text' in data else self._text

    def __repr__(self):
        return '<{!r} id={!r} name={!r} text={!r}>' \
            .format(self.__class__.__name__, self._id, self._name, self._text)
