import pymongo

from bson import ObjectId


class DatabaseWrapper(object):

    def __init__(self, collection, data_class):
        self._collection = collection
        self._data_class = data_class

    def create(self, data):
        data = self.sanitize_data(data)
        data['_id'] = ObjectId()

        self._collection.insert_one(data)
        return self._data_class(data)

    # This method should be overriden by child class
    def sanitize_data(self, data):
        raise NotImplementedError

    def save(self, obj):
        self._collection.update_one({'_id': obj._id}, {'$set': obj.serialize(update=True)})

    def find(self):
        doc = self._collection.find({}).sort('created', pymongo.DESCENDING)

        objs = []
        for obj in doc:
            objs.append(self._data_class(obj))

        return objs

    def find_one(self, obj_id):
        doc = self._collection.find_one({'_id': ObjectId(obj_id)})
        if not doc:
            return None

        return self._data_class(doc)

    def find_query(self, query):
        doc = self._collection.find(query)

        objs = []
        for obj in doc:
            objs.append(self._data_class(obj))

        return objs

    def delete(self, obj):
        self._collection.delete_one({'_id': obj._id})
