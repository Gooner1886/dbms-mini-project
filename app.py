import os
import time
from datetime import datetime
from flask import Flask, redirect, render_template, flash, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
import mysql.connector
from functools import wraps

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
app.run(debug=True)

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


def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/decide")
def decide():
    return render_template("decide.html", title = "Decide")


@app.route("/login", methods=['GET', 'POST'])
def login():
    cur = mydb.cursor()
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Query database for username
        qry = ("SELECT * FROM Customer WHERE Username=%s")
        cur.execute(qry, (username,))

        result = cur.fetchall()
        print(result)

        # Ensure username was submitted
        if not request.form.get("username"):
            error = "Must provide Username"

        # Ensure password was submitted
        elif not request.form.get("password"):
            error = "Must provide Password"

        # Ensure username exists and password is correct
        elif len(result) != 1 or not check_password_hash(result[0][2], password):
            print("invalid username and/or password")
            error = "Invalid Credentials"

        # Remember which user has logged in
        else:
            session["user_id"] = result[0][0]
            # Redirect user to home page
            print("Logged in Successfully!")
            return redirect("/decide")

        return render_template("login.html", error = error)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    cur = mydb.cursor()
    session.clear()

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


@app.route("/catalogue", methods = ["GET", "POST"])
def catalogue():
    cur = mydb.cursor()
    if request.method == "POST":
        ISBN = request.form["ISBN"]
        print(ISBN)
        now = datetime.now()
        print(now)
        insert_view = "INSERT INTO VIEWED(Account_ID, ISBN, Time_viewed) VALUES(%s, %s, %s)"
        viewval = (session["user_id"], ISBN, now)
        cur.execute(insert_view, viewval)
        mydb.commit()
        print("Book viewing details inserted")

        get_saleprice = "SELECT SalePrice, Book_name FROM Books WHERE ISBN = %s"
        isbn_val = (ISBN, )
        cur.execute(get_saleprice, isbn_val)
        rows = cur.fetchall()
        print(rows)

        insert_cart = "INSERT INTO CART(Account_ID, ISBN, Book_name, SalePrice) VALUES(%s, %s, %s, %s)"
        cartval = (session["user_id"], ISBN, rows[0][1], rows[0][0])
        cur.execute(insert_cart, cartval)
        mydb.commit()
        print("Cart details inserted")


        return redirect("/cart")
    else:
        cur = mydb.cursor()
        select_books = "SELECT * FROM Books"
        cur.execute(select_books)
        rows = cur.fetchall()
        lenrow = len(rows)
        print(lenrow)
        print(rows)
        get_balance = "SELECT Balance FROM Customer WHERE Account_ID = %s"
        current_session = (session["user_id"], )
        cur.execute(get_balance, current_session)
        bal = cur.fetchall()
        print(bal)
        return render_template("catalogue.html", title="Catalogue of Books", rows = rows, lenrow = lenrow, bal = bal)


@app.route("/cart", methods=["GET", "POST"])
def cart():
    cur = mydb.cursor()
    if request.method == "GET":
        select_cart = "SELECT * FROM Cart WHERE Account_ID=%s"
        cur.execute(select_cart, (session["user_id"],))
        cart = cur.fetchall()
        print(cart)
        cartlen = len(cart)

        cartprice = "SELECT SUM(SalePrice) FROM Cart WHERE Account_ID=%s"
        cur.execute(cartprice, (session["user_id"],))
        price=cur.fetchall()
        print(price)

        return render_template("cart.html", cart=cart, cartlen=cartlen, cartprice=price)
    elif request.method == "POST":
        CARTISBN = request.form["CARTISBN"]
        print(CARTISBN)
        deleteitem = "DELETE FROM Cart WHERE ISBN=%s"
        cur.execute(deleteitem, (CARTISBN, ))
        return redirect("/cart")


bookOrderIsbn = []
sellerlist=[]


@app.route("/payment", methods=["GET", "POST"])
def payment():
    cur = mydb.cursor()
    if request.method == "GET":
        select_cart = "SELECT * FROM Cart WHERE Account_ID=%s"
        cur.execute(select_cart, (session["user_id"],))
        cart = cur.fetchall()

        lenrow=len(cart)
        print("Checkout")
        print(cart)

        for i in range(lenrow):
            bookOrderIsbn.append(cart[i][2])
        print("Checkout")
        print(bookOrderIsbn)
        print(len(bookOrderIsbn))

        cartprice = "SELECT SUM(SalePrice) FROM Cart WHERE Account_ID=%s"
        cur.execute(cartprice, (session["user_id"],))
        price=cur.fetchall()
        return render_template("checkout.html", kart=cart, lenrow=lenrow, price=price)
    elif request.method == "POST":
        fetch_Seller = "SELECT Account_ID FROM SALE WHERE ISBN=%s"
        print(len(bookOrderIsbn))
        for i in range(len(bookOrderIsbn)):
            cur.execute(fetch_Seller, (bookOrderIsbn[i], ))
            sellers = cur.fetchall()
            print("sellers")
            print(sellers)
            sellerlist.append(sellers[0][0])
        print("sellerlist")
        print(sellerlist)

        # TransactionLogic
        cartprice = "SELECT SUM(SalePrice) FROM Cart WHERE Account_ID=%s"
        cur.execute(cartprice, (session["user_id"],))
        price=cur.fetchall()
        print("Price Fetched")
        money_from_buyer = "UPDATE Customer SET Balance= Balance - %s WHERE Account_ID=%s"
        cur.execute(money_from_buyer, (price[0][0], session["user_id"], ))
        mydb.commit()
        print("Money deducted from buyer")

        money_to_seller = "UPDATE Customer SET Balance= Balance + %s WHERE Account_ID=%s"
        insert_into_payment = "INSERT INTO PAYMENT(Account_ID, Seller_ID, Payment_Type, PaymentDate) values (%s, %s, %s, %s)"
        for i in range(len(sellerlist)):
            print("Entered Loop")
            bookSalePrice= "SELECT SalePrice FROM Books WHERE ISBN=%s"
            cur.execute(bookSalePrice, (bookOrderIsbn[i], ))
            print("Received Saleprice")
            bookprice = cur.fetchall()
            print(bookprice)
            cur.execute(money_to_seller, (bookprice[0][0], sellerlist[i]), )
            mydb.commit()
            print("Payment Seller Record Inserted")
            now = datetime.now()
            cur.execute(insert_into_payment, (session["user_id"], sellerlist[i], "PURCHASE", now ))
            mydb.commit()
            show_payment = "SELECT * FROM PAYMENT"
            cur.execute(show_payment)
            payments = cur.fetchall()
            print(payments)
            print("Payment Record Inserted")

            remove_from_cart="DELETE FROM CART WHERE Account_ID=%s AND ISBN=%s"
            cur.execute(remove_from_cart, (session["user_id"], bookOrderIsbn[i], ))
            mydb.commit()
            print("Removed from cart")
            remove_from_books="DELETE FROM Books WHERE ISBN=%s"
            cur.execute(remove_from_books, (bookOrderIsbn[i], ))
            mydb.commit()
            print("Removed from books")

        bookOrderIsbn.clear()
        return render_template("thankyou.html", title="Thank You")