from flask import Flask, render_template, request
from waitress import serve
from objects.user import User,SAMPLE_USERS



# Used this tutorial to figure out login screen 
#https://www.youtube.com/watch?v=R-hkzqjRMwM&ab_channel=NachiketaHebbar

app = Flask(__name__)

@app.route('/')
def set_up(): 
    return render_template('loginpage.html')

@app.route('/form_login', methods = ['POST','GET'])
def login():
    #temp solution untill database is up and running 
    get_name = request.form['username'] 
    get_password = request.form['password']
    for user in SAMPLE_USERS: # sample users is the sample data from User Class 
        if user.username == get_name and user.password == get_password:
            return render_template('index.html') 
    return render_template("loginpage.html", info = "Invalid Credentials") 

if __name__ == "__main__":
    serve(app, host = "0.0.0.0", port = 8000)

login()