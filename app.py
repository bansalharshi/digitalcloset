
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session

# import sqlite3
from cs50 import SQL

from helpers import apology, login_required

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
# @login_required
def index():
    print("bobo")
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

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

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")






# @app.route("/additem", methods=["GET", "POST"])
# # @login_required
# def additem():

#     return render_template("additem.html")

# @app.route("/")
# # @login_required
# def index():

#     return render_template("index.html")

