from flask import Flask, render_template, request
from waitress import serve
from objects.user import User,SAMPLE_USERS
import sqlite3


# Used this tutorial to figure out login screen 
#https://www.youtube.com/watch?v=R-hkzqjRMwM&ab_channel=NachiketaHebbar

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
    cursor.execute("SELECT username, password FROM user where (username = ? and password = ?)",(get_name, get_password))
    row = cursor.fetchall()
    connection.close()
    if len(row) == 1: 
        return render_template('index.html') 
    else:
        return render_template("loginpage.html", info = "Invalid Credentials") 

if __name__ == "__main__":
    serve(app, host = "0.0.0.0", port = 8000)

login()