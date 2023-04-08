from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from datetime import timedelta
import sqlite3


app = Flask(__name__)
"""bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'dkf3sldkjfDF23fLJ3b'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 10)"""


@app.route('/')
def home():
        return render_template("login.html")

        
app.run(host='0.0.0.0', port=81, debug=True)