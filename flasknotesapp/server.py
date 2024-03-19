from flask import Flask, render_template, request
from waitress import serve
import sqlite3
import re
import sys 
sys.path.append("databases")
import user_database


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

    if get_name.isdigit() == True:
        error_count += 1 
        username_message = 'invalid username entered'

    # Check if the email is valid 
    #https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/  # Used for email validification 
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(regex, get_email)):
        pass
    else:
        error_count += 1 
        email_message = "Invalid email entered"

    # Check if the password is too short: 
    if len(get_password) < 8:
        password_message = 'Password is too short' 

    # Check if the password and the confirmpassword are the same
    if get_password != get_confirmpassword:
        confirm_password_message = 'Passwords do not match'

    print("ERROR COUNT", error_count)

    is_account = True 

    if error_count == 0:
        # check if there is already an account 
        if is_account == True: 
            error_message = ("Account with those details already created, please login")
            return render_template('register.html', msg = error_message)
        else:
            return render_template('homepage.html')
    else: 
        return render_template('register.html',fname_error = fname_message, lname_error = lname_message, email_error = email_message, username_error = username_message,password_error = password_message, confirm_password_error = confirm_password_message)



    print("fname", get_fname, "\n",
          "lname", get_lname, "\n",
          "email", get_email, "\n",
          "username", get_name, "\n",
          "password", get_password, "\n",
          "confirmpassword", get_confirmpassword, "\n")

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

if __name__ == "__main__":
    serve(app, host = "0.0.0.0", port = 8000)
    checkdatabase()
    login()
