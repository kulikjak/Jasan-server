import datetime

from server.util import DatabaseWrapper


class Feedbacks(DatabaseWrapper):

    def __init__(self, model, db):
        super().__init__(db['feedbacks'], Feedback)

    def sanitize_data(self, data):
        return {
            'created': datetime.datetime.utcnow(),
            'title': data['title'],
            'text': data['text']
        }


class Feedback(object):

    def __init__(self, feedback):
        self._id = feedback['_id']
        self._created = feedback['created']
        self._title = feedback['title']
        self._text = feedback['text']

    def serialize(self, update=False):
        feedback = {
            'title': self._title,
            'text': self._text
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
        return self._created.isoformat()

    def __repr__(self):
        return f'<{self.__class__.__name__!r} id={self._id!r} title={self._title} created={self._created.isoformat()} text={self._text}>'
