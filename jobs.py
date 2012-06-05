from mongokit import Connection
from model import Activity, City
from datetime import datetime

if __name__ == '__main__':
    con = Connection()
    con.uppsalabarn.drop_collection("activities")
    con.uppsalabarn.drop_collection("cities")
    con.register([Activity, City])
    c1 = con.City()
    c1.name = u"Uppsala"
    c1.save()
    a1 = con.Activity()
    a1.name = u"Baddags"
    a1.starts_at = datetime.now()
    a1.city = c1
    a1.save()
