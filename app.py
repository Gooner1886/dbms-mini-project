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

""" mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="rootroot",
  database="thebookkeeper",
) """

mydb = mysql.connector.connect(
   host="localhost",
   user="root",
   password="Siddharth#52",
   database="dbmsminiproject"
)

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
        elif not request.form.get("F_name"):
            error = "Must enter First name"
        elif not request.form.get("L_name"):
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
            # Inserting username and password into database
            create_account = "INSERT INTO Customer(Username, Pass_word, F_name, L_name, Phone_No, Address, Email, Financial_status) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)" 
            val = (username,
                        generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8), request.form.get("F_name"), request.form.get("L_name"), request.form.get("Phone_No"), request.form.get("Address"), request.form.get("Email"), request.form.get("Financial_status"))
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
            
            

            return render_template('decide.html')
        return render_template('register.html', error=error)
    else:

        return render_template("register.html", title = "Register")
       
""" @app.route("/customer", methods = ["GET", "POST"]) 
def customer():
    cur = mydb.cursor()
    if request.method == "POST":
        counter = 0
        username = request.form.get("Username")
        password = request.form.get("Password")
        
        for c in username:
            counter = counter + 1

        # Ensure username was submitted
        if not request.form.get("Username"):
            error = 'Must Provide Username'

        # Ensure that username is between 2 and 15 characters
        elif counter < 2 or counter > 15:
            error = 'Username requirements are not met'

        # Ensure that password was submitted
        elif not request.form.get("Password"):
            error = 'Must Provide Password'
        elif not F_name:
            error = "Must enter First name"
        elif not L_name:
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
            create_account = "INSERT INTO Customer (Username, Pass_word, F_name, L_name, Phone_No, Address, Email, Financial_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cvalues = (username,
                        generate_password_hash(password, method='pbkdf2:sha256', salt_length=8), F_name, L_name, request.form.get("Phone_No"), request.form.get("Address"), request.form.get("Email"), request.form.get("Financial_status"))
            cur.execute(create_account, cvalues)
            mydb.commit()

            print(cur.rowcount, "Customer Record inserted")

            return render_template("decide.html")
        return render_template("customerdetails.html", error = error)                            
    else:
        return render_template("customerdetails.html") """

@app.route("/bookdetails", methods=["GET", "POST"])
def bookdetails():
    cur = mydb.cursor()
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("ISBN"):
            error = 'Must Provide ISBN'
        elif not request.form.get("Book_name"):
            error = 'Must Provide Book_name'
        elif not request.form.get("Genre"):
            error = 'Must Provide Genre'
        elif not request.form.get("Author"):
            error = 'Must Provide Author'
        elif not request.form.get("MRP"):
            error = 'Must Provide MRP'
        elif not request.form.get("SalePrice"):
            error = 'Must Provide Sale Pricec'
        elif not request.form.get("Description"):
            error = 'Must Provide Description'                         
        else:
            # Inserting username and password into database
            list_book = "INSERT INTO Books(ISBN, Book_name, Genre, Author, MRP, SalePrice, Description) VALUES(%s, %s, %s, %s, %s, %s, %s)" 
            bookval = (request.form.get("ISBN"), request.form.get("Book_name"), request.form.get("Genre"), request.form.get("Author"), request.form.get("MRP"), request.form.get("SalePrice"), request.form.get("Description"))
            cur.execute(list_book, bookval) 
            mydb.commit()
            print(cur.rowcount, "book record inserted.")

            fill_sale = "INSERT INTO SALE(Account_ID, ISBN) VALUES (%s, %s)"
            saleval = (session["user_id"], request.form.get("ISBN"))
            cur.execute(fill_sale, saleval)
            mydb.commit()
            print(cur.rowcount, "sale record inserted")
            return render_template("thankyou.html")
        return render_template("bookdetails.html", error=error)

    return render_template("bookdetails.html", title="Book Details")

@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html", title="Thank You")    
