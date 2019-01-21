import datetime

from server.util import DatabaseWrapper


class Feedbacks(DatabaseWrapper):

    def __init__(self, model, db):
        super().__init__(db['feedbacks'], Feedback)

    def sanitize_data(self, data):
        return {
            'title': data['title'],
            'text': data['text']
        }


class Feedback(object):

    def __init__(self, feedback):
        self._id = feedback['_id']
        self._title = feedback['title']
        self._text = feedback['text']

    def serialize(self):
        return {
            'title': self._title,
            'text': self._text
        }

    def toJson(self):
        return {
            'id': str(self._id),
            'created': self._id.generation_time,
            'title': self._title,
            'text': self._text
        }

    @property
    def id(self):
        return str(self._id)

    @property
    def title(self):
        return self._title

    @property
    def text(self):
        return self._text

    @property
    def created(self):
        return self._id.generation_time

    def __repr__(self):
        return f'<{self.__class__.__name__!r} id={self._id!r} title={self._title} created={self._created.isoformat()} text={self._text}>'
