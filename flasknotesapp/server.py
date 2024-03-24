import os
import requests
import sys
#pip install iPython
from IPython.display import display, HTML
sys.path.append("objects")
from onedrive import generate_access_token, GRAPH_API_ENDPOINT
from flask import Flask, render_template, request
from waitress import serve
import sqlite3
import re
sys.path.append("databases")
import user_database
import numpy as np 


# Used this tutorial to figure out login screen 
#https://www.youtube.com/watch?v=R-hkzqjRMwM&ab_channel=NachiketaHebbar

#used this for the sql request for placeholders, https://medium.com/@miguel.amezola/protecting-your-code-from-sql-injection-attacks-when-using-raw-sql-in-python-916466961c97


app = Flask(__name__)

def checkdatabase():
    user_database.create_database() #call the function that creates the database

@app.route('/')
def set_up(): 
    return render_template('loginpage.html')

@app.route('/form_login', methods = ['POST','GET'])
def login():
    get_name = request.form['username'] 
    get_password = request.form['password']
    connection = sqlite3.connect("user.db")
    cursor =  connection.cursor()
    cursor.execute("SELECT username, password FROM user where (username = ? and password = ?)",(get_name.strip(), get_password.strip()))
    row = cursor.fetchall()
    connection.close()
    if len(row) == 1: 
        return render_template('homepage.html') 
    else:
        error_message = "Incorrect Username or Password!"
        return render_template("loginpage.html", msg = error_message) 

@app.route('/register')
def register(): 
    return render_template("register.html")

@app.route('/form_register',  methods = ['POST','GET'])
def register_actions():

    error_count = 0

    fname_message = ""
    lname_message = ""
    email_message = ""
    username_message = ""
    password_message = ""
    confirm_password_message = ""
    get_fname = request.form['fname']
    get_lname = request.form['lname']
    get_email = request.form['email']
    get_name = request.form['username'] 
    get_password = request.form['password']
    get_confirmpassword = request.form['confirmpassword']

    print("fname", get_fname, "\n",
      "lname", get_lname, "\n",
      "email", get_email, "\n",
      "username", get_name, "\n",
      "password", get_password, "\n",
      "confirmpassword", get_confirmpassword, "\n")

    # Check if there are numbers in the first name

    for character in [*get_fname]: 
        if character.isdigit():
            error_count += 1 
            fname_message = 'invalid first name entered (no numbers)'
            break

    # Check if there are numbers in the last name

    for character in [*get_lname]: 
        if character.isdigit():
            error_count += 1 
            lname_message = 'invalid last name entered (no numbers)'
            break

    # Check if username is already taken 

    connection = sqlite3.connect("user.db")
    cursor =  connection.cursor()
    cursor.execute("SELECT username FROM user where username = ?",(get_name,))
    row = cursor.fetchall()
    connection.close()
    if len(row) ==  1:
        error_count += 1 
        username_message = 'Username is already taken'

    # Check if the email is valid 
    #https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/  # Used for email validification 

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(regex, get_email)):
        pass
    else:
        error_count += 1 
        email_message = "Invalid email entered"

    # Check if the password meets criterua with length being >= 9 and having a number and special character: 

    criteria_length = 9 
    criteria_number = 1 
    password_num_count = 0 
    criteria_special = 1 
    password_special_count = 0 
    special_characters = ['!','@','#','$','%','^','&','*','<','>','?']

    if len(get_password) < 10:
        password_message = 'Password does not meet criteria' 
    else: 
        for character in [*get_password]:
            if character.isdigit(): 
                password_num_count +=1 
            else: 
                pass
            if character in special_characters: 
                password_special_count +=1 
            else: 
                pass

    if criteria_number < password_num_count: 
        password_message = 'Password does not meet criteria' 
    else: 
        pass
    if criteria_special < password_special_count:
        password_message = 'Password does not meet criteria' 
    else: 
        pass 

    # Check if the password and the confirmpassword are the same
    if get_password != get_confirmpassword:
        confirm_password_message = 'Passwords do not match'

    print("ERROR COUNT", error_count)

    # Check if email is associated with account already, if so send them to login / forgot password 

    connection = sqlite3.connect("user.db")
    cursor =  connection.cursor()
    cursor.execute("SELECT email FROM user where email = ?",(get_email,))
    row = cursor.fetchall()
    connection.close()
    if len(row) == 1: 
        is_account = True 
    else:
        is_account = False 

    # Returns the correct page
    # ERROR COUNT > 1 -> Page with criteria messages
    # Email already in systmem -> MSG saying go to login or forgot password
    # No error -> to homepage  

    if error_count == 0: 
        if is_account == True: 
            error_message = ("Account with that email has alreday been created, please proceed to login. ")
            return render_template('register.html', msg = error_message)
        else:
            #create user id (placeholder untill I can figure something more useful)
            id_num =np.random.randint(0,99,2)
            get_user_id = get_lname + str(id_num[0]) + str(id_num[1])
            connection = sqlite3.connect("user.db")
            cursor =  connection.cursor()
            cursor.execute("INSERT INTO user VALUES (?,? ,? ,?)",(get_user_id,get_name, get_password, get_email,))
            connection.commit()
            connection.close()
            return render_template('homepage.html')
    else: 
        return render_template('register.html',fname_error = fname_message, lname_error = lname_message, email_error = email_message, username_error = username_message,password_error = password_message, confirm_password_error = confirm_password_message)


@app.route('/forgotpsd')
def forgot_password():
    return render_template("forgot_pswd.html")

@app.route('/upload')
def upload_page(): 
    return render_template("upload.html")

@app.route('/group')
def group_page():
    return render_template("groups.html")

@app.route('/favorite')
def favorite_page():
    return render_template("favorite.html")

@app.route('/logout')
def logoutpage_page():
    os.remove("ms_graph_api_token.json")
    return render_template("logoutpage.html")

@app.route('/onedrive')
def onedrive():
    APP_ID = '5e84b5a7-fd04-4398-a15f-377e3d85703e'
    SCOPES = ['Files.ReadWrite']
    access_token = generate_access_token(APP_ID, SCOPES)
    headers = {
        'Authorization': 'Bearer ' + access_token['access_token']
    }
    return render_template("homepage.html")

if __name__ == "__main__":
    serve(app, host = "0.0.0.0", port = 8000)
    checkdatabase()
    login()

# Check if the group name is a duplicate in the database
def check_for_duplicate_group(group_name):
    connection = sqlite3.connect("group.db")
    cursor = connection.cursor()
    cursor.execute("SELECT group_name FROM groups WHERE group_name = ?", (group_name,))
    existing_group = cursor.fetchone()
    connection.close()
    return existing_group is not None

@app.route('/form_create_group', methods=['POST'])
def create_group():
    # Get form data
    group_name = request.form['group_name']

    # Check for duplicate group name
    if check_for_duplicate_group(group_name):
        error_message = "Create the group with a different name"
        return render_template("create_group.html", error_message=error_message)
    else:
        # If group name is unique, continue with group creation logic
        # Your group creation logic here
        return "Group successfully created"

if __name__ == "__main__":
    app.run(debug=True)