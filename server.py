from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

import sqlite3, os, json
from src.dbQueries import dbQueries

path = os.path.dirname(os.path.realpath(__file__))

conn = sqlite3.connect(path + "/bikes.db")

application = Flask(__name__)


@application.route("/")
def hello():
    return render_template("home.html")

@application.route('/api')
def api():
    return "usage: api/rack?racknum = YOUR_NUM"

@application.route('/api/rack')   
def rack():
#     db has to be inside function otherwise error about db being created in anohter thread
    db = dbQueries("bikes.db")  
    racknum = request.args.get('racknum')
    max_racknum = db.num_bike_stations()
    if int(racknum) > max_racknum:
        # http://flask.pocoo.org/docs/0.10/patterns/errorpages/
        return render_template('404.html'), 404
    else:
        return racknum

# Just adding a route to pull down static data. This can be adjusted later
@application.route('/api/static')
def static_api():
    # open db connection
    conn = sqlite3.connect(path + "/bikes.db")

    c = conn.cursor()
    data = c.execute("SELECT number, name, address, position_lat, position_long, banking FROM static ORDER BY number")
    data = data.fetchall()
    # convert to array of dictionaries
    for i in range(0, len(data)):
        data[i] = {
            "number": data[i][0],
            "name": data[i][1],
            "address": data[i][2],
            "position": {
                "lat": data[i][3],
                "lang": data[i][4]
            },
            "banking": data[i][5] == 'True'
        }

    # close db connection
    conn.close()
    return json.dumps(data)

@application.route('/api/station/<id>')
@application.route('/api/station/<id>/<day>')
def historical_data (id, day = None):
    """
    gets historical data for a station by id. Used by the client side
    """
    # get all station information by id.
    database = dbQueries("bikes.db")
    if day:
        info = database.get_historical_info_by_id_and_day(id, day)
    else:
        info = database.get_historical_info_by_id(id)

    # states that database usage is finished
    database.close_connection()

    return json.dumps(info)


@application.route('/station/address')
def station (address):
    """
    Gets station information based on the address and loads the appropriate static template
    """
    pass

@application.route('/about')
def about():
    data = [
        {
            "id": 1,
            "name": "Some aname"

        },

        {
            "id": 2,
            "name": "Some aname2"

        },

        {
            "id": 2,
            "name": "Some aname3"

        }
    ]

    return render_template('test.html', mData = data)


if __name__ == "__main__":
    application.debug = True
    application.run(host='0.0.0.0')
    
# localhost:5000/api?racknum=1
