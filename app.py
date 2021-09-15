import os

import time
from datetime import datetime

from flask import Flask, redirect, render_template, flash, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
""" from flask_mysqldb import MySQL """
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

import mysql.connector



mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Siddharth#52",
  database="project"
)

print(mydb) 

cur = mydb.cursor()


app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response




# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


""" app.config['MySQL_HOST'] = 'localhost'
app.config['MySQL_USER'] = 'root'
app.config['MySQL_PASSWORD'] = 'Siddharth#52'
app.config['MySQL_DB'] = 'project """

""" mysql = MySQL(app) """


@app.route("/")
def home():
    return "Hello, World!"

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":

        counter = 0
        username = request.form.get("username")
        for c in username:
            counter = counter + 1;

        # Ensure username was submitted
        if not request.form.get("username"):
            error = 'Must Provide Username'

        # Ensure that username is between 2 and 15 characters
        elif counter < 2 or counter > 15:
            error = 'Username requirements are not met'

        # Ensure that password was submitted
        elif not request.form.get("password"):
            error = 'Must Provide Password'

        # Ensure that confirmation password was submitted
        elif not request.form.get("confirmation"):
            error = 'Must Provide Confirmation'


        # Ensuring confirmation password matches password
        elif request.form.get("confirmation") != request.form.get("password"):
            error = 'Confirmation does not match Password'

        else:
            

            # Inserting username and password into database
            create_account = "INSERT INTO Account (username, pass_word) VALUES (%s, %s)" 
            val = (request.form.get("username"),
                        generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8))
            cur.execute(create_account, val)
            """ cur.execute("SELECT * FROM Account")

            myresult = cur.fetchone()

            
            print(myresult) """
            mydb.commit()
            print(cur.rowcount, "record inserted.")
            

            return render_template('register.html')
        return render_template('register.html', error=error)
    else:

        return render_template("register.html", title = "Register")    
