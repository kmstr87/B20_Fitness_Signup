from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from datetime import timedelta
import sqlite3

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'dkf3sldkjfDF23fLJ3b'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 10)


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

@app.route('/success/<username>')
def success(username):
    return render_template("user_profile.html", name=username)

@app.route('/login', methods=['POST', 'GET'])
def login():

        if (request.method == "GET"):
                return render_template("login.html")
        else:
                if "form-login" in request.form:
                        username = request.form['uname']
                        password = request.form['psw']
                        #get the cursor (a pointer to the DB)
                        sql_query = "SELECT username, password FROM USER WHERE "
                        sql_query += "username = '" + username + "';"
                        #execute the query and commit the results
                        con = sqlite3.connect("database.db")
                        cur = con.cursor()
                        rows = cur.execute(sql_query).fetchall()
                        
                        if(len(rows) == 0):
                                flash("No such user: " + username)
                                return render_template("login.html")
                        #rows[0] is the row containing the username/password
                        #so rows[0][1] is the password value
                        hashedpwd = rows[0][1]
                        if(not bcrypt.check_password_hash(hashedpwd, password)):
                                flash("Sorry, wrong password")
                                return render_template("login.html")
                        else:    
                                return redirect(url_for('success', username=username))
                        
                elif "form-register" in request.form:
                        username = request.form['new_uname']
                        password = request.form['new_psw']
                        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
                        email = request.form['email']
                        #print(username + ":" + password)
                        try:
                                #get the cursor (a pointer to the DB)
                                sql_query = "INSERT INTO User VALUES ('"
                                sql_query += username + "','" + pw_hash + "','" + email + "')"
                                #execute the query and commit the results
                                con = sqlite3.connect("database.db")
                                cur = con.cursor()
                                cur.execute(sql_query)
                                con.commit()
                                flash("User successfully added")
                                return redirect(url_for('home'))
                        except sqlite3.IntegrityError:
                                flash("Username already exists")
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