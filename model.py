import datetime

import pymongo
import bson

pymongo.objectid = bson.objectid
import mongokit

class Document(mongokit.Document):
    __database__ = "uppsalabarn"
    use_dot_notation = True

class City(Document):
    __collection__ = "cities"
    structure = {
        'name': unicode
    }
    required_fields = ['name']

class Activity(Document):
    __collection__ = "activities"
    structure = {
        'name': unicode,
        'starts_at': datetime.datetime,
        'city' : City
    }
    required_fields = ['name', 'starts_at', 'city']


