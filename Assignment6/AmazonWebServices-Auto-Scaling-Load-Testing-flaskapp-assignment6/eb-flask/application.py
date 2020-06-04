from flask import Flask, request, render_template
import pandas as pd
import os
from math import radians, degrees, cos, sin, asin, sqrt
import csv, base64, time
import pymysql



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


@application.route("/update", methods=["POST", "GET"])
def update():
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

    return render_template("update.html", rows1=rows1, rows2=rows2, rows5=rows5,rows6=rows6, rows7=rows7, elapsed_time=elapsed_time)


if __name__ == "__main__":
    application.debug = True
    application.run()