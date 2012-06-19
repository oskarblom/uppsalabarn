from mongoengine import Document, StringField, DateTimeField, ReferenceField
import datetime
import hashlib

class Activity(Document):
    name = StringField(required=True)
    starts_at = DateTimeField(required=True)
    city = StringField(required=True)
    description = StringField()

    def __unicode__(self):
        return unicode(vars(self))

    def checksum(self):
        d = self.starts_at.date() if hasattr(self.starts_at, "date") else self.starts_at
        return hashlib.md5(self.name.encode("utf8") + str(d)).hexdigest()

