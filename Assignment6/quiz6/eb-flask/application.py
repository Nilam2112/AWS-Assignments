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

count = 0
@application.route("/")
def home():
    global count
    count = count + 1
    pagetime = datetime.datetime.now()
    # return render_template('home.html', count=count, pagetime=pagetime)
    return render_template('home.html')



@application.route("/greaterthan", methods=["POST", "GET"])
def greaterthan():
    # range1 = float(request.form['range1'])
    range1 = int(request.form['range1'])
    # name = str(request.form['name'])
    # name1 = str(request.form['name1'])

    start_time = time.time()

    sql1 = "SELECT VolcanoName,Latitude,Longitude FROM quiz.Volcano WHERE  Num ='" + str(range1) + "'"

    cursor.execute(sql1)
    rows1 = cursor.fetchall()

    end_time = time.time()
    elapsed_time = end_time-start_time

    return render_template("greaterthan.html", rows=rows1,elapsed_time=elapsed_time)


@application.route("/withinrange", methods=["POST", "GET"])
def withinrange():
    range1 = str(request.form['range1'])
    name1 = str(request.form['name1'])

    sql1 = "UPDATE quiz.Volcano SET VolcanoName = '" + str(name1) + "' WHERE Num = '" + str(range1) + "'"
    sql2 = "SELECT VolcanoName,Latitude,Longitude FROM quiz.Volcano WHERE Num = '" + str(range1) + "' and VolcanoName = '" + str(name1) + "'"
    cursor.execute(sql1)
    cursor.execute(sql2)
    rows1 = cursor.fetchall()


    return render_template("withinrange.html", rows=rows1, rowcount=len(rows1))

@application.route("/setpage", methods=["POST", "GET"])
def setpage():
    start_time = time.time()
    # range1 = str(request.form['range1'])
    # range2 = str(request.form['range2'])
    #
    # sql1 = "UPDATE quiz.Volcano SET VolcanoName = '" + str(range2) + "' WHERE Num = '" + str(range1) + "'"
    # sql2 = "SELECT * FROM quiz.Volcano WHERE Num = '" + str(range1) + "'"
    # cursor.execute(sql1)
    # cursor.execute(sql2)
    # rows1 = cursor.fetchall()

    # end_time = time.time()
    # elapsed_time = end_time - start_time
    elapsed_time = start_time
    return render_template("setpage.html",elapsed_time=elapsed_time)

@application.route("/update", methods=["POST", "GET"])
def update():
    range1 = float(request.form['range1'])
    range2 = float(request.form['range2'])
    range3 = float(request.form['range3'])
    range4 = float(request.form['range4'])
    # startdate = (request.form['startdate'])
    # enddate = (request.form['enddate'])
    # mag = float(request.form['mag'])
    # num = int(request.form['mag'])

    start_time = time.time()

    # sql1 = "UPDATE quiz.quake SET mag = '" + str(mag) + "'  WHERE depth BETWEEN '" + str(range1) + "' AND '" + str(range2) + "' AND time BETWEEN '" + str(startdate) + "%' AND '" + str(enddate) + "%'"
    sql1 = "SELECT Num,Country,Latitude,Longitude FROM quiz.Volcano  WHERE Latitude BETWEEN '" + str(range1) + "' AND '" + str(range2) + "' AND Longitude BETWEEN '" + str(range3) + "' AND '" + str(range4) + "'"
    cursor.execute(sql1)
    rows1 = cursor.fetchall()
    # sql2 = "SELECT * FROM dbo.quakes WHERE depth between '" + str(range1) + "' AND '" + str(range2) + "' AND GMTTIME BETWEEN '" + str(startdate) + "%' AND '" + str(enddate) + "%'"
    # cursor.execute(sql2)
    # rows2 = cursor.fetchall()

    end_time = time.time()
    elapsed_time = end_time-start_time

    # return render_template("update.html", elapsed_time=elapsed_time)
    return render_template("update.html", rows=rows1, elapsed_time=elapsed_time)
    # return render_template("update.html", rows=rows2, rowcount=len(rows2), elapsed_time=elapsed_time)


@application.route("/update1", methods=["POST", "GET"])
def update1():
    sid = int(request.form['sid'])
    course = int(request.form['course'])
    section = int(request.form['section'])

    start_time = time.time()

    sql1 = "SELECT IdNum FROM quiz.students WHERE IdNum = '" + str(sid) + "'"
    cursor.execute(sql1)
    rows1 = cursor.fetchall()

    sql2 = "SELECT Maximum FROM quiz.Fall2019 WHERE Course = '" + str(course) + "' AND Section = '" + str(section) + "' AND Maximum <> 0"
    cursor.execute(sql2)
    rows2 = cursor.fetchall()

    if rows1 and rows2 is not None:
        sql3 = "UPDATE quiz.Fall2019 SET Maximum = Maximum-1 WHERE Course = '" + str(course) + "' AND Section = '" + str(section) + "'"
        cursor.execute(sql3)
        sql4 = "INSERT INTO quiz.stco VALUES ('" + str(sid) + "', '" + str(course) + "', '" + str(section) + "')"
        cursor.execute(sql4)

    sql5 = "SELECT Maximum FROM quiz.Fall2019 WHERE Course = '" + str(course) + "' AND Section = '" + str(section) + "'"
    cursor.execute(sql5)
    rows5 = cursor.fetchall()

    sql6 = "SELECT * FROM quiz.stco"
    cursor.execute(sql6)
    rows6 = cursor.fetchall()

    sql7 = "SELECT sc.IdNum, sc.Course, sc.Section, c.Maximum FROM quiz.students as s, quiz.Fall2019 as c, quiz.stco as sc WHERE sc.IdNum=s.IdNum AND sc.Course=c.Course AND sc.Section=c.Section"
    cursor.execute(sql7)
    rows7 = cursor.fetchall()

    end_time = time.time()
    elapsed_time = end_time-start_time

    return render_template("update1.html", rows1=rows1, rows2=rows2, rows5=rows5,rows6=rows6, rows7=rows7, elapsed_time=elapsed_time)


#
# if __name__ == "__main__":
#     application.debug = True
#     application.run()

port = os.getenv('PORT', '8082')
if __name__ == '__main__':
     application.debug = True
     application.run(host='0.0.0.0', port=int(port))
