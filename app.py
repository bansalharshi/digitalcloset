
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session

# import sqlite3
from cs50 import SQL

from helpers import apology, login_required, usd

# using datetime module to get current date and time
from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///closet.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    # print(session)
    #print(session["user_id"])
    all_items = db.execute(
        "SELECT name, notes, brand, weblink, case when imagelink = '' then '../static/default_image.jpg' else imagelink end as imagelink from items WHERE user_id = ?", session["user_id"])

    if len(all_items)==0:
        return render_template("no_items.html")
    else:
        return render_template("index.html", all_items=all_items)

    
@app.route("/clothes", methods=["GET"])
@login_required
def clothes():
    # print("bobo")
    all_clothes = db.execute(
        "SELECT name, notes, brand, weblink, case when imagelink = '' then '../static/default_image.jpg' else imagelink end as imagelink from items WHERE type = 'Clothes' AND user_id = ?", session["user_id"])

    if len(all_clothes)==0:
        return render_template("no_clothes.html")
    else:
        return render_template("clothes.html", all_clothes = all_clothes)


@app.route("/shoes", methods=["GET"])
@login_required
def shoes():
    # print("bobo")
    all_shoes = db.execute(
        "SELECT name, notes, brand, weblink, case when imagelink = '' then '../static/default_image.jpg' else imagelink end as imagelink from items WHERE type = 'Shoes' AND user_id = ?", session["user_id"])


    if len(all_shoes)==0:
        return render_template("no_shoes.html")
    else:
        return render_template("shoes.html", all_shoes = all_shoes)

@app.route("/accessories", methods=["GET"])
@login_required
def accessories():
    all_accessories = db.execute(
        "SELECT name, notes, brand, weblink, case when imagelink = '' then '../static/default_image.jpg' else imagelink end as imagelink from items WHERE type = 'Accessories' AND user_id = ?", session["user_id"])


    if len(all_accessories)==0:
        return render_template("no_accessories.html")
    else:
        return render_template("accessories.html", all_accessories = all_accessories)



@app.route("/history", methods=["GET"])
@login_required
def history():
    itemprices = db.execute(
        "SELECT name, purchase_date, weblink, case when (purchase_price = '' or typeof(purchase_price) <> 'integer') then 0 else purchase_price end as purchase_price, brand, type from items WHERE user_id = ?", session["user_id"])
                # "SELECT name, purchase_date, weblink, purchase_price, brand, type from items WHERE user_id = ?", session["user_id"])
    
    # print(itemprices)

    # print(itemprices["purchase_price"])

    # print(type(itemprices["purchase_price"]))

    total_price = sum(itemprice["purchase_price"] for itemprice in itemprices)
    # total_price = 0

    for itemprice in itemprices:
        if itemprice["purchase_price"] == 0 or type(itemprice["purchase_price"]) != int:
            itemprice["purchase_price"] = "Price not recorded"
        else:
            itemprice["purchase_price"] = usd(itemprice["purchase_price"])
            # total_price += total_price

    if total_price == 0:
        total_price = "No price recorded"
    else:
        total_price = usd(total_price)

    # print(total_price)

    return render_template("history.html", itemprices=itemprices, total_price = total_price)    



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    print("login")

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        print("username")

        print(request.form.get("username"))

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        print(rows)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

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
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # First check if all the 3 fields have an input
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)

        print(request.form.get("username"))

        # Second check if the username is an existing username
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        print(rows)
        print(type(rows))

        if len(rows) != 0:
            return apology("username already exists", 400)

        # Third check if password == confirmation
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("password must be same as confirmation", 400)

        # If no errors are found then add the row to the database
        # First generate password hash

        username = request.form.get("username")
        hash = generate_password_hash(request.form.get("password"))

        print(username)
        print(hash)

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        current_id = db.execute("SELECT MAX(id) as id FROM users")
        # print (current_id)

        session["user_id"] = current_id[0]["id"]

        # return redirect("/add_item")
        return render_template("additem.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")






@app.route("/additem", methods=["GET", "POST"])
@login_required
def additem():
    type_list = ["Clothes", "Shoes", "Accessories"]

    # print(type_list)
    # print(type(type_list))

    """If user submits an item"""
    if request.method == "POST":
        name = request.form.get("name")
        brand = request.form.get("brand")
        imagelink = request.form.get("imagelink")
        purchase_price = request.form.get("purchase_price")
        type = request.form.get("type")
        weblink = request.form.get("weblink")
        notes = request.form.get("notes")

        # cdt = datetime.now()
        # cd = cdt.date()
        # ct = cdt.strftime("%H:%M:%S")
        print("data loaded")

        db.execute("INSERT INTO items (user_id, name, imagelink, purchase_price, type, weblink, notes, brand, purchase_date, purchase_time) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"], name, imagelink, purchase_price, type, weblink, notes, brand, datetime.now().date(), datetime.now().strftime("%H:%M:%S"))

        # print("data inserted")
        #check if we should keep of drop the column logging date
        #check if the purchase date anf purchase time should be remaned to logging date and logging time
        # return redirect("/")
        return render_template("additem.html", type_list = type_list)

    else:

        return render_template("additem.html", type_list = type_list)



