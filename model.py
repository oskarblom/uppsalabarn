from mongoengine import Document, StringField, DateTimeField, ReferenceField, queryset_manager
import datetime
import hashlib

class Activity(Document):
    name = StringField(required=True)
    starts_at = DateTimeField(required=True)
    city = StringField(required=True)
    source = StringField(required=True)
    description = StringField()
    url = StringField()
    email = StringField()
    phone = StringField()

    @queryset_manager
    def old(cls, queryset):
        today = datetime.datetime.combine(datetime.date.today(), datetime.time())
        return queryset.filter(starts_at__lt=today)

    def __unicode__(self):
        return unicode(vars(self))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __ne__(self, other):
        return self.__hash__() != other.__hash__()

    def __hash__(self):
        d = self.starts_at.date() if hasattr(self.starts_at, "date") else self.starts_at
        md5 = hashlib.md5(self.name.encode("utf8") + str(d)).hexdigest()
        return int(md5, 16)
