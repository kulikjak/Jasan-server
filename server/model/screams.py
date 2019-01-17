import datetime

from server.util import DatabaseWrapper


class Screams(DatabaseWrapper):

    def __init__(self, model, db):
        super().__init__(db['screams'], Scream)

    def sanitize_data(self, data):
        return {
            'created': datetime.datetime.utcnow(),
            'name': data['name'],
            'text': data['text'],
            'user_id': data['user_id'],
            'attachment': data['attachment'],
            'popularity': None
        }


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

    @property
    def id(self):
        return str(self._id)

    @property
    def name(self):
        return self._name

    @property
    def text(self):
        return self._text

    @property
    def created(self):
        return self._created.isoformat()

    @property
    def user_id(self):
        return self._user_id

    @property
    def attachment(self):
        return self._attachment

    @property
    def thumbnail(self):
        path, ext = self._attachment.split('.')
        return f'{path}_thumbnail.{ext}'

    @property
    def popularity(self):
        return self._popularity if self._popularity else 0

    @popularity.setter
    def popularity(self, value):
        self._popularity = value

    def __repr__(self):
        return f'<{self.__class__.__name__!r} id={self._id!r} name={self._name} text={self._text}>'
