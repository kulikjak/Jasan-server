import pymongo

from bson import ObjectId


class Polls(object):

    COLLECTION_NAME = 'polls'

    def __init__(self, model, db):
        self._model = model
        self._db = db
        self._collection = db[self.COLLECTION_NAME]

    def create_poll(self, data):

        poll = Poll({'_id': ObjectId(), 'title': data['title'], 'public': data['public']})
        self._collection.insert_one(poll.serialize())

        return poll

    def save(self, poll):
        self._collection.update_one({'_id': poll._id}, {'$set': poll.serialize(update=True)})

    def delete(self, poll):
        self._collection.delete_one({'_id': poll._id})

    def find(self):
        doc = self._collection.find({})

        polls = []
        for poll in doc:
            polls.append(Poll(poll))

        return polls

    def find_one(self, poll_id=None):
        query = {}
        if poll_id is not None:
            query['_id'] = ObjectId(poll_id)

        doc = self._collection.find_one(query)
        if not doc:
            return None

        return Poll(doc)


class Poll(object):

    def __init__(self, poll):
        self._id = poll['_id']
        self._title = poll['title']
        self._public = poll['public']
        self._responses = []

    def serialize(self, update=False):

        poll = {'title': self._title, 'public': self._public}

        if not update:
            poll['_id'] = self._id

        return poll

    def get_serialized_data(self):
        return {'id': str(self._id), 'title': self._title, 'public': self._public}

    def get_id(self):
        return str(self._id)

    def get_title(self):
        return self._title

    def get_responses(self):
        return self._responses

    def is_public(self):
        return self._public

    def extract_responses(self, responses):
        for response in responses:
            if response._poll_id == self.get_id():
                self._responses.append(response)

    def set_title(self, title):
        return self._title

    def set_public(self, status):
        self._public = status

    def set_data(self, data):
        self._title = data['title']
        self._public = data['public']

    def __repr__(self):
        return '<{!r} id={!r} title={!r} public={!r}>' \
            .format(self.__class__.__name__, self._id, self._title, self._public)
