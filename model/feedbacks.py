import datetime
import pymongo

from bson import ObjectId


class Feedbacks(object):

    COLLECTION_NAME = 'feedbacks'

    def __init__(self, model, db):
        self._model = model
        self._db = db
        self._collection = db[self.COLLECTION_NAME]

    def create_feedback(self, data):

        feedback = Feedback({
            '_id': ObjectId(),
            'created': datetime.datetime.utcnow(),
            'title': data['title'],
            'text': data['text'],
            'user_id': data['user_id']
        })
        self._collection.insert_one(feedback.serialize())

        return feedback

    def save(self, feedback):
        self._collection.update_one(
            {
                '_id': feedback._id
            }, {
                '$set': feedback.serialize(update=True)
            })

    def delete(self, feedback):
        self._collection.delete_one({'_id': feedback._id})

    def find(self):
        doc = self._collection.find({}).sort('created', pymongo.DESCENDING)

        feedbacks = []
        for feedback in doc:
            feedbacks.append(Feedback(feedback))

        return feedbacks


class Feedback(object):

    def __init__(self, feedback):
        self._id = feedback['_id']
        self._created = feedback['created']
        self._title = feedback['title']
        self._text = feedback['text']
        self._user_id = feedback['user_id']

    def serialize(self, update=False):
        feedback = {
            'title': self._title,
            'text': self._text,
            'user_id': self._user_id
        }
        if not update:
            feedback['_id'] = self._id
            feedback['created'] = self._created

        return feedback

    def get_serialized_data(self):
        return {
            'id': str(self._id),
            'created': self._created.isoformat(),
            'title': self._title,
            'text': self._text,
            'user_id': self._user_id
        }

    def get_id(self):
        return str(self._id)

    def get_title(self):
        return self._title

    def get_text(self):
        return self._text

    def get_user_id(self):
        return self._user_id

    def get_created(self):
        return self._created.isoformat()

    def __repr__(self):
        return '<{!r} id={!r} title={!r} created={!r} text={!r}>' \
            .format(self.__class__.__name__, self._id, self._title, self._created.isoformat(), self._text)
