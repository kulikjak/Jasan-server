import datetime

from flask_login import UserMixin

from server.util import DatabaseWrapper


class Users(DatabaseWrapper):

    def __init__(self, model, db):
        super().__init__(db['users'], User)

    def sanitize_data(self, data):
        return {
            'name': data['name'],
            'password': data['password'],
            'active': data['active'],
            'admin': data['admin']
        }


class User(UserMixin):

    def __init__(self, user):
        self._id = user['_id']
        self._name = user['name']
        self._password = user['password']
        self._active = user['active']
        self._admin = user['admin']

    def serialize(self):
        return {
            'name': self._name,
            'password': self._password,
            'active': self._active,
            'admin': self._admin
        }

    def toJson(self):
        return {
            'id': str(self._id),
            'created': self._id.generation_time,
            'name': self._name,
            'password': self._password,
            'active': self._active,
            'admin': self._admin
        }

    # Flask related methods
    def get_id(self):
        return str(self._id)

    def is_active(self):
        return self._active

    @property
    def id(self):
        return str(self._id)

    @property
    def created(self):
        return self._id.generation_time

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active):
        self._active = active

    @property
    def admin(self):
        return self._admin

    @admin.setter
    def admin(self, admin):
        self._admin = admin

    def __repr__(self):
        return f'<{self.__class__.__name__!r} id={self._id!r} name={self._name}>'
