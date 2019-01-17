import datetime

from server.util import DatabaseWrapper


class Emails(DatabaseWrapper):

    def __init__(self, model, db):
        super().__init__(db['emails'], Email)

    def sanitize_data(self, data):
        return {
            'source': data['source'],
            'destination': data['destination'],
            'metadata': data['metadata'],
            'subject': data['subject'],
            'body': data['body']
        }


class Email(object):

    def __init__(self, email):
        self._id = email['_id']
        self._source = email['source']
        self._destination = email['destination']
        self._metadata = email['metadata']
        self._subject = email['subject']
        self._body = email['body']

    def serialize(self, update=False):
        email = {
            'source': self._source,
            'destination': self._destination,
            'metadata': self._metadata,
            'subject': self._subject,
            'body': self._body
        }
        if not update:
            email['_id'] = self._id

        return email

    def get_serialized_data(self):
        return {
            'id': str(self._id),
            'created': self._created.isoformat(),
            'source': self._source,
            'destination': self._destination,
            'metadata': self._metadata,
            'subject': self._subject,
            'body': self._body
        }

    @property
    def id(self):
        return str(self._id)

    @property
    def created(self):
        return self._id.generation_time

    @property
    def source(self):
        return self._source

    @property
    def destination(self):
        return self._destination

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        self._metadata = metadata

    @property
    def subject(self):
        return self._subject

    @property
    def body(self):
        return self._body

    def __repr__(self):
        return f'<{self.__class__.__name__!r} id={self._id!r} source={self._source} destination={self._destination} subject={self._subject}>'
