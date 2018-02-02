import pymongo

from bson import ObjectId


class Responses(object):

    COLLECTION_NAME = 'responses'

    def __init__(self, model, db):
        self._model = model
        self._db = db
        self._collection = db[self.COLLECTION_NAME]

    def create_response(self, data):

        response = Response({
            '_id': ObjectId(),
            'poll_id': data['poll_id'],
            'value': int(data['value']),
            'text': data['text']
        })
        self._collection.insert_one(response.serialize())

        return response

    def save(self, response):
        self._collection.update_one(
            {
                '_id': response._id
            }, {
                '$set': response.serialize(update=True)
            })

    def delete(self, response):
        self._collection.delete_one({'_id': response._id})

    def find(self):
        doc = self._collection.find({})

        responses = []
        for response in doc:
            responses.append(Response(response))

        return responses


class Response(object):

    def __init__(self, response):
        self._id = response['_id']
        self._poll_id = response['poll_id']
        self._value = response['value']
        self._text = response['text']

    def serialize(self, update=False):

        response = {'poll_id': self._poll_id, 'value': self._value, 'text': self._text}

        if not update:
            response['_id'] = self._id

        return response

    def get_serialized_data(self):
        return {
            'id': str(self._id),
            'poll_id': self._poll_id,
            'value': self._value,
            'text': self._text
        }

    def get_id(self):
        return str(self._id)

    def get_text(self):
        return self._text

    def get_value(self):
        return self._value

    def get_poll_id(self):
        return self._poll_id

    def __repr__(self):
        return '<{!r} id={!r} poll_id={!r} text={!r}' \
            .format(self.__class__.__name__, self._id, self._poll_id, self._text)
