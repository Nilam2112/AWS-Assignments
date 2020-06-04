from flask import Flask, request, render_template
import os
from math import radians, degrees, cos, sin, asin, sqrt
import csv, base64, time
import pymysql
import datetime
from flask import Flask,render_template,request
import time


application = Flask(__name__)

db = pymysql.connect(user='',
                     password='',
                     host='',
                     cursorclass=pymysql.cursors.DictCursor)
# Enter user, password and host. Deleted for security purposes
cursor = db.cursor()


@application.route("/")
def home():
    return render_template('home.html')


@application.route("/greaterthan", methods=["POST", "GET"])
def greaterthan():
    range1 = float(request.form['range1'])

    start_time = time.time()

    sql1 = "SELECT * FROM quiz.quake WHERE mag > '" + str(range1) + "'"
    cursor.execute(sql1)
    rows1 = cursor.fetchall()

    end_time = time.time()
    elapsed_time = end_time-start_time

    return render_template("greaterthan.html", rows=rows1, rowcount=len(rows1), elapsed_time=elapsed_time)


@application.route("/withinrange", methods=["POST", "GET"])
def withinrange():
    range1 = float(request.form['range1'])
    range2 = float(request.form['range2'])

    start_time = time.time()

    sql1 = "SELECT * FROM quiz.quake WHERE mag between '" + str(range1) + "' AND '" + str(range2) + "'"
    cursor.execute(sql1)
    rows1 = cursor.fetchall()

    end_time = time.time()
    elapsed_time = end_time-start_time

    return render_template("withinrange.html", rows=rows1, rowcount=len(rows1), elapsed_time=elapsed_time)


@application.route("/update", methods=["POST", "GET"])
def update():
    range1 = float(request.form['range1'])
    range2 = float(request.form['range2'])
    startdate = (request.form['startdate'])
    enddate = (request.form['enddate'])
    mag = float(request.form['mag'])

    start_time = time.time()

    sql1 = "UPDATE quiz.quake SET mag = '" + str(mag) + "'  WHERE depth BETWEEN '" + str(range1) + "' AND '" + str(range2) + "' AND time BETWEEN '" + str(startdate) + "%' AND '" + str(enddate) + "%'"
    cursor.execute(sql1)

    # sql2 = "SELECT * FROM dbo.quakes WHERE depth between '" + str(range1) + "' AND '" + str(range2) + "' AND GMTTIME BETWEEN '" + str(startdate) + "%' AND '" + str(enddate) + "%'"
    # cursor.execute(sql2)
    # rows2 = cursor.fetchall()

    end_time = time.time()
    elapsed_time = end_time-start_time

    return render_template("update.html", elapsed_time=elapsed_time)
    # return render_template("update.html", rows=rows2, rowcount=len(rows2), elapsed_time=elapsed_time)


# def haversine(lon1, lat1, lon2, lat2):
#     # """
#     # Calculate the great circle distance between two points
#     # on the earth (specified in decimal degrees)
#     # """
#     # convert decimal degrees to radians
#     lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
#
#     # haversine formula
#     dlon = lon2 - lon1
#     dlat = lat2 - lat1
#     a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
#     c = 2 * asin(sqrt(a))
#     r = 6371 # Radius of earth in kilometers. Use 3956 for miles
#     return c * r
#
#
def bounding_box(lat, lon, distance):
    # Input and output lats/longs are in degrees.
    # Distance arg must be in same units as RADIUS.
    # Returns (dlat, dlon) such that
    # no points outside lat +/- dlat or outside lon +/- dlon
    # are <= "distance" from the (lat, lon) point.
    # Derived from: http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates
    # WARNING: problems if North/South Pole is in circle of interest
    # WARNING: problems if longitude meridian +/-180 degrees intersects circle of interest
    # See quoted article for how to detect and overcome the above problems.
    # Note: the result is independent of the longitude of the central point, so the
    # "lon" arg is not used.
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    dlat = distance / r
    dlon = asin(sin(dlat) / cos(radians(lat)))
    return degrees(dlat), degrees(dlon)


@application.route("/latlon", methods=["POST", "GET"])
def latlon():
    lat = float(request.form['latitude'])
    lon = float(request.form['longitude'])
    distance = float(request.form['distance'])

    start_time = time.time()

    newlat, newlon = bounding_box(lat, lon, distance)

    sql1 = "SELECT * FROM quiz.quake WHERE latitude between '" + str(lat) + "' AND '" + str(newlat) + "' AND longitude between '" + str(lon) + "' and '" + str(newlon) + "'"
    cursor.execute(sql1)
    rows1 = cursor.fetchall()

    end_time = time.time()
    elapsed_time = end_time-start_time

    return render_template("latlon.html", rows=rows1, rowcount=len(rows1), elapsed_time=elapsed_time)


@application.route('/new', methods=['GET', 'POST'])
def new():
    start = datetime.datetime.now()
    b = start.second
    if (b % 2) == 0:
        return render_template('index_m.html', dt=str(start))
    else:
        return render_template('index1_m.html', dt=str(start))
    return render_template("index_m.html", dt=str(start))

@application.route('/kmeans', methods=['GET', 'POST'])
def main():
    cursor = db.cursor()
    success = 'SELECT Age,Fare from minnow'
    cursor.execute(success)

    result = cursor.fetchall()
    return render_template('searchearth.html', ci=result)



if __name__ == "__main__":
    application.debug = True
    application.run()