from mongoengine import Document, StringField, DateTimeField, ReferenceField
import datetime
import hashlib

class City(Document):
    name = StringField(required=True)

class Activity(Document):
    name = StringField(required=True)
    #description = StringField(required=True)
    date = DateTimeField(required=True)
    city = StringField(required=True)

    def __unicode__(self):
        return unicode(vars(self))

    def save(self, *args, **kwargs):
        self.checksum = hashlib.md5(self.name.encode("utf8") + str(self.date)).hexdigest() 
        return super(Activity, self).save(*args, **kwargs)

