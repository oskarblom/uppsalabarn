#from gevent import monkey; monkey.patch_all()
from flask import Flask, render_template
from model import Activity
from mongoengine import connect
import datetime
#import gevent

app = Flask(__name__)

@app.route("/")
def index():
    today = datetime.datetime.combine(datetime.date.today(), datetime.time())
    acts = Activity.objects(starts_at__gte=today)
    app.logger.debug(acts)
    return render_template("index.html", acts=acts)

if __name__ == '__main__':
    connect("uppsalabarn")
    #app.run(debug=True)
    app.run()

