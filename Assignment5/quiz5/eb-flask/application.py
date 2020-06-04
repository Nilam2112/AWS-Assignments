
import pymysql
from flask import Flask,render_template,request


application = Flask(__name__)

db = pymysql.connect(user='',
                     password='',
                     host='',
                     cursorclass=pymysql.cursors.DictCursor)
# Enter user, password and host. Deleted for security purposes
cursor = db.cursor()


@application.route("/")
def home():
    return render_template('1.html')


if __name__ == "__main__":
    application.debug = True
    application.run()