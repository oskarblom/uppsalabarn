from gevent import monkey; monkey.patch_all()
from BeautifulSoup import BeautifulSoup
from datetime import datetime, date, timedelta, time
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

    dates = (date.today() + timedelta(days=i) for i in range(1))

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
            act.source = "untguiden"

            header = item_soup.find("h1")
            act.name = header.find(text=True).strip()
            act.description = re.sub(r"^%s" % act.name, "", header.parent.text, count=1).strip()

            url = item_soup.find("strong", text="Webb")
            if url:
                act.url = url.parent.findNextSibling("a")["href"].strip()

            email = item_soup.find("strong", text="E-post")
            if email:
                act.email = email.parent.findNextSibling("a").find(text=True).strip()

            phone = item_soup.find("strong", text="Kontakt")
            if phone:
                act.phone = re.sub(r"^Kontakt: ", "", phone.parent.parent.text).strip()

            act.starts_at = datetime.datetime.combine(act_date, time())
            activities.append(act)

    return activities

def destinationuppsala():
    log.debug("Getting activities from destionation uppsala")
    activities = []
    base_url = "http://www.destinationuppsala.se"

    desclabel_re = re.compile("Description$")
    phonelabel_re = re.compile("Phone$")
    urllabel_re = re.compile("Web$")
    emaillabel_re = re.compile("Email$")

    dates = (date.today() + timedelta(days=i) for i in range(1))

    for act_date in dates:
        eventlist_url = "%s/DynPage.aspx?id=9582&search=true&start=%s&end=%s&cat=9&txt=" % (base_url, act_date, act_date)
        list_doc = urllib2.urlopen(eventlist_url).read()
        list_soup = BeautifulSoup(list_doc)
        event_urls = (item["href"] for item in list_soup.findAll("a", "evListObject"))

        for url in event_urls:
            item_url = "%s/%s" % (base_url, url)
            item_doc = urllib2.urlopen(item_url).read()
            item_soup = BeautifulSoup(item_doc, fromEncoding="utf-8")

            act = Activity(city="uppsala")
            act.source = "destinationuppsala"
            act.name = item_soup.find("font", "head1").find(text=True).strip()

            desc = item_soup.find("span", id=desclabel_re)
            if desc:
                desc_text = desc.find(text=True)
                if desc_text:
                    act.description = desc_text.strip()

            phone = item_soup.find("span", id=phonelabel_re)
            if phone:
                act.phone = phone.text.replace("Tfn:", "").strip()

            url = item_soup.find("span", id=urllabel_re)
            if url:
                act.url = url.find("a")["href"].strip()

            email = item_soup.find("span", id=emaillabel_re)
            if email:
                act.email = email.find("a").find(text=True).strip()

            act.starts_at = datetime.datetime.combine(act_date, time())
            activities.append(act)

    return activities

if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)

    jobs = [gevent.spawn(j) for j in (untguiden, destinationuppsala)]

    connect("uppsalabarn")

    deleted = [a.delete() for a in Activity.old()]
    log.debug("Deleted %d old activities" % len(deleted))

    gevent.joinall(jobs)

    current_activities = set(Activity.objects())
    parsed_activities = set(itertools.chain(*(job.value for job in jobs)))
    new_activities = parsed_activities - current_activities

    log.debug("Current act length: %s" % len(current_activities))
    log.debug("Parsed act length: %s" % len(parsed_activities))

    [act.save() for act in new_activities]
