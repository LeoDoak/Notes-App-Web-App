from flask import Flask, render_template, request
from waitress import serve
from objects.user import User,SAMPLE_USERS
import sqlite3


# Used this tutorial to figure out login screen 
#https://www.youtube.com/watch?v=R-hkzqjRMwM&ab_channel=NachiketaHebbar

#used this for the sql request for placeholders, https://medium.com/@miguel.amezola/protecting-your-code-from-sql-injection-attacks-when-using-raw-sql-in-python-916466961c97


app = Flask(__name__)

@app.route('/')
def set_up(): 
    return render_template('loginpage.html')

@app.route('/form_login', methods = ['POST','GET'])
def login():
    get_name = request.form['username'] 
    get_password = request.form['password']
    connection = sqlite3.connect("databases/user.db")
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

@app.route('/forgotpsd')
def forgot_password():
    return render_template("forgot_pswd.html")

if __name__ == "__main__":
    serve(app, host = "0.0.0.0", port = 8000)
login()