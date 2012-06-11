from gevent import monkey; monkey.patch_all()
from BeautifulSoup import BeautifulSoup
from datetime import date, timedelta
from model import *
from mongoengine import connect
import gevent
import urllib2
import itertools

def untguiden():
    activities = []
    base_url = "http://untguiden.teknomedia.se"

    startdate = date.today()
    dates = (startdate + timedelta(days=i) for i in range(7))

    for act_date in dates:
        eventlist_url = "%s/Default.aspx?action=search&c=3443&d=%s" % (base_url, act_date)
        list_doc = urllib2.urlopen(eventlist_url).read()
        list_soup = BeautifulSoup(list_doc)
        event_urls = (item.find("a")["href"] for item in list_soup.findAll("div", "Event"))

        for url in event_urls:
            item_url = "%s%s" % (base_url, url)
            item_doc = urllib2.urlopen(item_url).read()
            item_soup = BeautifulSoup(item_doc)
            act = Activity(date=act_date, city="uppsala")
            act.name = item_soup.find("h1").find(text=True)
            activities.append(act)

    return activities

def do_thing2():
    a = Activity(name=u"Bogus act", date=datetime.date.today(), city=u"uppsala")
    return [a]

if __name__ == '__main__':
    jobs = [gevent.spawn(j) for j in (untguiden, do_thing2)]
    print "jobs spawned"
    gevent.joinall(jobs)

    connect("uppsalabarn")
    Activity.drop_collection()
    activities = (job.value for job in jobs)
    for act in itertools.chain(*activities):
        act.save()
        print act.checksum
