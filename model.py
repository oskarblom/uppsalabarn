#coding=utf-8
from mongoengine import Document, StringField, DateTimeField, ReferenceField, queryset_manager
import datetime
import hashlib
import re

slug_re = re.compile(u"[^A-ZÅÄÖa-zåäö0-9 ]")

class Activity(Document):
    name = StringField(required=True)
    starts_at = DateTimeField(required=True)
    city = StringField(required=True)
    source = StringField(required=True)
    description = StringField()
    url = StringField()
    email = StringField()
    phone = StringField()
    slug = StringField()
    original_url = StringField()

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

    def save(self, *args, **kwargs):
        charmap = {
            u"å": u"a",
            u"ä": u"a",
            u"ö": u"o",
            u" ": u"-"
        }
        self.slug = re.sub(slug_re, "", self.name).lower()
        for key, val in charmap.iteritems():
            self.slug = self.slug.replace(key, val)
        self.slug = "%s-%s" % (self.slug, self.starts_at.date())

        return super(Activity, self).save(*args, **kwargs)
