from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from datetime import timedelta
import sqlite3
from flask_mail import Mail

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'dkf3sldkjfDF23fLJ3b'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 10)

#connect to the SQL Database
con = sqlite3.connect("database.db")
cur = con.cursor()

# Creates the User table
user_query = """
    CREATE TABLE IF NOT EXISTS User 
    (
        username TEXT PRIMARY KEY, 
        password TEXT,
        email TEXT
    )
"""

# Creates the Contacts table
contacts_query = """
    CREATE TABLE IF NOT EXISTS Contacts
    (
        email TEXT PRIMARY KEY, 
        name TEXT,
        message TEXT
    )
"""

# Executing the commands
cur.execute(user_query)
cur.execute(contacts_query)

# Routing to home page and rendering when GET request is sent
@app.route('/')
def home():
        return render_template("home.html")        

# Routing to /macros/<username> page. Render the template when GET request is sent;
# Access the information sent through form, calc. calories needed and outputing the msg while rerouting for POST
@app.route('/macros/<username>', methods=['GET', 'POST'])
def macros(username):
        if (request.method == "GET"):
                flash("")
                return render_template("user_profile.html", username=username)
        else:
                # Getting info from form
                height = request.form['height']
                weight = request.form['weight']
                sex = request.form['sex']
                age = request.form['age']
                goal = request.form['fitness']
                BMR = 0

                # Calc. calories needed
                match goal:
                        case "Gain weight":
                                goalModifier = 500 
                        case "Lose weight":
                                goalModifier = -500 
                        case _:
                                goalModifier = 0

                ###### Add the equeation used to calculate the macros below
                if(sex == 'male'):
            
                        BMR = 88.362 + (13.397 * float(weight)) + (4.799 * float(height)) - (5.677 * float(age))
            
            
                else:
            
                        BMR = 447.593 + (9.247 * float(weight)) + (3.098 * float(height)) - (4.330 * float(age))
            
                dailyCal = round((BMR * 1.5) + goalModifier)    
                outputMsg = 'You will need ' + str(dailyCal) + ' calories to meet your goal!'
                # Outputing result and reroute
                flash(outputMsg)
                return redirect(url_for('macros', username=username))
        
# Routing to /login page. Render the template when GET request is sent;
# Insert the info. sent through form when register form is through POST.
# Reroute the user to /macros when the info. given through login form matches.
@app.route('/login', methods=['POST', 'GET'])
def login():
        # Rendering the template
        if (request.method == "GET"):
                return render_template("login.html")
        else:
                # For login
                if "form-login" in request.form:
                        # Get the info from form
                        username = request.form['uname']
                        password = request.form['psw']
                        #get the cursor (a pointer to the DB)
                        sql_query = "SELECT username, password FROM USER WHERE "
                        sql_query += "username = '" + username + "';"
                        #execute the query and commit the results
                        con = sqlite3.connect("database.db")
                        cur = con.cursor()
                        rows = cur.execute(sql_query).fetchall()
                        # No user found
                        if(len(rows) == 0):
                                flash("No such user: " + username)
                                return render_template("login.html")
                        #rows[0] is the row containing the username/password
                        #so rows[0][1] is the password value
                        hashedpwd = rows[0][1]
                        if(not bcrypt.check_password_hash(hashedpwd, password)):
                                flash("Sorry, wrong password")
                                return render_template("login.html")
                        # User found
                        else:    
                                return redirect(url_for('macros', username=username))
                # For registration form
                elif "form-register" in request.form:
                        # Get info from form
                        username = request.form['new_uname']
                        password = request.form['new_psw']
                        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
                        email = request.form['email']
                        # Insert values into Users table
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
                                return render_template("login.html")
                        # Failed
                        except sqlite3.IntegrityError:
                                flash("Username already exists")
                                return render_template("login.html")

# Rendering template for /calendar
@app.route('/calendar')
def calendar():
        return render_template("calendar.html")

# Routing to /contacts page. Render the template when GET request is sent;
# Insert the info. to Contacts table where info is sent through form
# when register form is through POST.
@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
        # Rendering the template
        if (request.method=='GET'):
                return render_template("contacts.html")
        else:
                # Get the info from form
                email = request.form['email']
                name = request.form['name']
                message = request.form['message']
                try:
                        #get the cursor (a pointer to the contacts table in DB)
                        sql_query = "INSERT INTO Contacts VALUES ('"
                        sql_query += email + "','" + name + "','" + message + "')"
                        #execute the query and commit the results to db
                        con = sqlite3.connect("database.db")
                        cur = con.cursor()
                        cur.execute(sql_query)
                        con.commit()
                        flash("Message has been sent!")
                        return render_template("contacts.html")
                # Failed to add
                except sqlite3.IntegrityError:
                        flash("Failed to send the information.")
                        return render_template("contacts.html")


"Extra Pages to be added"

# Rendering template for /tutorial
@app.route('/tutorials')
def tutorials():
        return render_template("tutorials.html")

# Rendering template for /about
@app.route('/about')
def about():
        return render_template("about.html")

# Running the server
app.run(host='0.0.0.0', port=81, debug=True)