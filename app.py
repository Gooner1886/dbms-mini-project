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
  password="rootroot",
  database="thebookkeeper",
)

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="Siddharth#52",
#   database="project"
# )

print(mydb)


app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True


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
    return render_template("home.html")

@app.route("/decide")
def decide():
    return render_template("decide.html" , title = "Decide")

@app.route("/login", methods = ['GET', 'POST'])
def login():

    """Log user in"""

    # Forget any user_id
    session.clear()


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        username_val = request.form.get("username")
        check_account = "SELECT * FROM Customer WHERE Username = %s"
        
        rows = cur.execute(check_account, username_val)
        mydb.commit()

        # Ensure username was submitted
        if not request.form.get("username"):
            error = 'Must Provide Username'

        # Ensure password was submitted
        elif not request.form.get("password"):
            error = 'Must Provide Password'

        # Ensure username exists and password is correct
        elif len(rows) != 1 or not check_password_hash(rows[0]["Pass_word"], request.form.get("password")):
            error = 'Invalid Credentials'

        else:
            # Remember which user has logged in
            session["user_id"] = rows[0]["Account_ID"]

            # Redirect user to home page
            return redirect("/decide.html")

        return render_template("login.html", error = error)


    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", title = "Log In")    


@app.route("/register", methods=["GET", "POST"])
def register():
    cur = mydb.cursor()
    if request.method == "POST":
        counter = 0
        username = request.form.get("username")
        for c in username:
            counter = counter + 1

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
            create_account = "INSERT INTO Customer (Username, Pass_word) VALUES (%s, %s)" 
            val = (request.form.get("username"),
                        generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8))
            cur.execute(create_account, val) 
            mydb.commit()
            print(cur.rowcount, "authentication record inserted.")

            select_session = "SELECT Account_ID FROM Customer WHERE Username = %s"
            curr_username = (request.form.get("username"), )
            print(curr_username)
            cur.execute(select_session, curr_username)
            rows = cur.fetchall()
            for row in rows:
                print(row)
            session["user_id"] = rows[0][0]
            print(session["user_id"])
            mydb.close()
            

            return render_template('customerdetails.html')
        return render_template('register.html', error=error)
    else:

        return render_template("register.html", title = "Register")  

@app.route("/customer", methods = ["GET", "POST"]) 
def customer():
    cur = mydb.cursor()
    if request.method == "POST":
        if not request.form.get("F_name"):
            error = "Must enter First name"
        elif not request.form.get("L_Name"):
            error = "Must enter Last name" 
        elif not request.form.get("Email"):
            error = "Must enter Email Address"
        elif not request.form.get("Phone_No"):
            error = "Must enter Phone Number"
        elif not request.form.get("Address"):
            error = "Must enter address"
        elif not request.form.get("Financial_status"):
            error = "Must enter financial status"
        else:
            insert_cdetails = "INSERT INTO Customer(F_Name, L_name, Phone_No, Address, Email, Financial_status) VALUES (%s, %s, %s, %s, %s, %s) WHERE Account_Id = %s"
            cvalues = (request.form.get("F_name"), request.form.get("L_Name"), request.form.get("Email"), request.form.get("Phone_No"), request.form.get("Address"), request.form.get("Financial_status"), session["user_id"])
            cur.execute(insert_cdetails, cvalues)
            mydb.commit()

            print(cur.rowcount, "Customer Record inserted")

            return render_template("decide.html")
        return render_template("customerdetails.html", error = error)                            
    else:
        return render_template("customerdetails.html")

@app.route("/bookdetails")
def bookdetails():
    return render_template("bookdetails.html", title="Details")