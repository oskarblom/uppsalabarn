from mongoengine import Document, StringField, DateTimeField, ReferenceField
import datetime
import hashlib

class Activity(Document):
    name = StringField(required=True)
    date = DateTimeField(required=True)
    city = StringField(required=True)

    def __unicode__(self):
        return unicode(vars(self))

    def checksum(self):
        return hashlib.md5(self.name.encode("utf8") + str(self.date)).hexdigest()

