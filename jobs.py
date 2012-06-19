from gevent import monkey; monkey.patch_all()
from BeautifulSoup import BeautifulSoup
from datetime import date, timedelta
from model import *
from mongoengine import connect
import gevent
import itertools
import logging
import re
import urllib2

log = logging.getLogger("jobs")

def untguiden():
    log.debug("Getting activities from untguiden")
    activities = []
    base_url = "http://untguiden.teknomedia.se"

    startdate = date.today()
    dates = (startdate + timedelta(days=i) for i in range(1))

    for act_date in dates:
        eventlist_url = "%s/Default.aspx?action=search&c=3443&d=%s" % (base_url, act_date)
        list_doc = urllib2.urlopen(eventlist_url).read()
        list_soup = BeautifulSoup(list_doc)
        event_urls = (item.find("a")["href"] for item in list_soup.findAll("div", "Event"))

        for url in event_urls:
            item_url = "%s%s" % (base_url, url)
            item_doc = urllib2.urlopen(item_url).read()
            item_soup = BeautifulSoup(item_doc)

            act = Activity(city="uppsala")
            header = item_soup.find("h1")
            act.name = header.find(text=True)
            act.description = re.sub(r"^", "", header.parent.text, count=1)
            act.starts_at = datetime.datetime.combine(act_date, datetime.time())
            activities.append(act)

    return activities

def temp():
    return []

if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)

    jobs = [gevent.spawn(j) for j in (untguiden, temp)]
    gevent.joinall(jobs)

    connect("uppsalabarn")
    current_activities = Activity.objects()

    today = datetime.datetime.combine(datetime.date.today(), datetime.time())
    deleted = [a.delete() for a in current_activities if a.starts_at < today]
    log.debug("Deleted %s old activities", len(deleted))

    for act in itertools.chain(*(job.value for job in jobs)):
        if not any(a.checksum() == act.checksum() for a in current_activities):
            act.save()
            log.debug("Saved new activity %s", act)
