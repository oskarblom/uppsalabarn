#from gevent import monkey; monkey.patch_all()
from flask import Flask, render_template, abort
from model import Activity
from mongoengine import connect
import datetime
#import gevent

app = Flask(__name__)

@app.route("/")
def activities():
    today = datetime.datetime.combine(datetime.date.today(), datetime.time())
    acts = Activity.objects(starts_at__gte=today)
    app.logger.debug(acts)
    return render_template("activities.html", acts=acts)

@app.route("/activity/<string:slug>")
def activity(slug):
    act = Activity.objects(slug=slug)
    if not act:
        abort(404)
    app.logger.debug(act)
    return "%s slug was passed" % act

if __name__ == '__main__':
    connect("uppsalabarn")
    app.run(debug=True)
    #app.run()

