from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from datetime import timedelta
import sqlite3

app = Flask(__name__)
bcrypt = Bcrypt(app)
"""bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'dkf3sldkjfDF23fLJ3b'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 10)"""

#connect to the SQL Database
con = sqlite3.connect("database.db")
cur = con.cursor()
# Creates the User table
sql_query = """
    CREATE TABLE IF NOT EXISTS User 
    (
        username TEXT PRIMARY KEY, 
        password TEXT,
        email TEXT
    )
"""
cur.execute(sql_query)

@app.route('/')
def home():
        return render_template("home.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
        if (request.method == "GET"):
                return render_template("login.html")


@app.route('/calendar')
def calendar():
        return render_template("calendar.html")

@app.route('/contacts')
def contacts():
        return render_template("contacts.html")

"Extra Pages to be added"

@app.route('/tutorials')
def tutorials():
        return render_template("tutorials.html")

@app.route('/about')
def about():
        return render_template("about.html")

        
app.run(host='0.0.0.0', port=81, debug=True)