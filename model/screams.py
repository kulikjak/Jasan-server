import pymongo

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
            'device': data['device'],
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
        self._device = scream['device']
        self._name = scream['name']
        self._text = scream['text']

    def serialize(self, update=False):
        scream = {'name': self._name, 'text': self._text}

        if not update:
            scream['_id'] = self._id
            scream['created'] = self._created
            scream['device'] = self._device

        return scream

    def get_serialized_data(self):
        return {
            'id': str(self._id),
            'created': self._created.isoformat(),
            'device': self._device,
            'name': self._name,
            'text': self._text
        }

    def get_id(self):
        return str(self._id)

    def set_name(self, text):
        self._text = data['text']

    def __repr__(self):
        return '<{!r} id={!r} name={!r} text={!r}>' \
            .format(self.__class__.__name__, self._id, self._name, self._text)
