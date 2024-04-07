""" Main Server Page  """

import os
import sqlite3
import json
import flask
import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_required, login_user, logout_user, LoginManager
from flask_wtf import FlaskForm
from waitress import serve
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField
from databases import user_database
from objects.onedrive import generate_access_token, GRAPH_API_ENDPOINT
from objects.user import User

# Don't know if we need 2 of these.

# Used this tutorial to figure out login screen
# https://www.youtube.com/watch?v=R-hkzqjRMwM&ab_channel=NachiketaHebbar

# used this for the sql request for placeholders,
# https://medium.com/@miguel.amezola/protecting-your-code-from-sql-injection-attacks-when-using-raw-sql-in-python-916466961c97
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['UPLOAD_FOLDER'] = 'static\\files'
# app.config['UPLOAD_FOLDER'] = 'static/files' (*mac)
app.secret_key = '''967b75c111e64965848a7786bda9602
        f9d208f991036ccc4f793a4199a9f74b4'''

# ACCESS_TOKEN = ""  "Global variable that flake8 does not like"

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Summary or Description of the function

    Parameters:

    Returns:
    object: User
    None
    """

    connection = sqlite3.connect("user.db")
    cursor = connection.cursor()
    cursor.execute(
        """SELECT user_id, username, password,
        email FROM user where (user_id = ?)""",
        (user_id,))
    row = cursor.fetchall()
    connection.close()
    if len(row) == 1:
        return User(row[0][0], row[0][1], row[0][2], row[0][3])
    return None


def checkdatabase():
    """Summary or Description of the function

    Parameters:

    Returns:
    object: User
    None
    """

    # call the function that creates the database
    user_database.create_database()


@app.route('/')
def set_up():
    """Summary or Description of the function

    Parameters:

    Returns:
    object: User
    None
    """

    return render_template('loginpage.html')


@app.route('/form_login', methods=['POST', 'GET'])
def login():
    """Summary or Description of the function

    Parameters:

    Returns:
    object: User
    None
    """

    get_name = request.form['username']
    get_password = request.form['password']
    current_user = User(None, get_name, get_password, None)
    if current_user.is_authenticated():
        flask.flash('Logged in successfully.')
        current_user.set_login_user_id()
        current_user.set_login_email()
        login_user(current_user)
        # next = flask.request.args.get('next')
        return redirect(url_for('homepage'))
    error_message = "Incorrect Username or Password!"
    return render_template("loginpage.html", msg=error_message)


@app.route('/homepage')
@login_required
def homepage():
    """Summary or Description of the function

    Parameters:

    Returns:
    object: User
    None
    """

    return render_template("homepage.html")


@app.route('/register')
def register():
    """Summary or Description of the function

    Parameters:

    Returns:
    object: User
    None
    """

    return render_template("register.html")


@app.route('/form_register', methods=['POST', 'GET'])
def register_actions():
    """Summary or Description of the function

    Parameters:

    Returns:
    object: User
    None
    """

    get_email = request.form['email']
    get_name = request.form['username']
    get_password = request.form['password']
    get_confirmpassword = request.form['confirmpassword']

    # create new user
    new_user = User(None, get_name, get_password, get_email)

    # check user
    (username_message, email_message, password_message,
        confirm_password_message, register_status) = new_user.check_new_user(get_confirmpassword)

    if register_status is False:
        print("not able to regster")
        return render_template(
            "register.html",
            email_error=email_message, username_error=username_message,
            password_error=password_message,
            confirm_password_error=confirm_password_message)
    print("registered")
    flask.flash('Logged in successfully.')
    login_user(new_user)
    return render_template('homepage.html')


@app.route('/forgotpsd')
def forgot_password():
    """Summary or Description of the function

    Parameters:

    Returns:
    object: User
    None
    """

    return render_template("forgot_pswd.html")


class UploadFileForm(FlaskForm):
    """Summary or Description of the function

    Parameters:

    Returns:
    object: User
    None
    """
    file = FileField("File")
    submit = SubmitField("Upload File")

    def method1(self):
        """Placeholder method 1."""
        # placeholder
        print("Method 1")

    def method2(self):
        """Placeholder method 2."""
        # placeholder
        print("Method 2")


@app.route('/upload', methods=['GET', "POST"])
@login_required
def upload_page():
    """Summary or Description of the function

    Parameters:

    Returns:
    object: User
    None
    """
    timeout = 60
    headers = onedrive()
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(
            os.path.join(os.path.abspath(os.path.dirname(__file__)),
                         app.config['UPLOAD_FOLDER'],
                         secure_filename(file.filename)))
        dir_list = os.listdir('static\\files')
        #  headers = {
        #    'Authorization': 'Bearer ' + access_token['access_token']
        #  }
        for file_path in dir_list:
            name = file_path
            file_path = 'static\\files\\' + file_path
            with open(file_path, 'rb') as upload:
                media_content = upload.read()
                response = requests.put(
                    GRAPH_API_ENDPOINT +
                    f'/me/drive/items/root:/{name}:/content',
                    headers=headers,
                    data=media_content,
                    timeout=timeout
                )
                print(response.json())
        return render_template("homepage.html")
    return render_template("upload.html", form=form)


@app.route('/group')
@login_required
def group_page():
    """Summary or Description of the function

    Parameters:

    Returns:
    object: User
    None
    """

    return render_template("groups.html")


@app.route('/group_details')
@login_required
def group_details_page():
    # Get the value of the 'title' query parameter
    group_name = request.args.get('title', 'Default Group Name')
    return render_template("group_details.html", group_name=group_name)


@app.route('/favorite')
@login_required
def favorite_page():
    """Summary or Description of the function

    Parameters:

    Returns:
    object: User
    None
    """
    return render_template("favorite.html")


@app.route('/logout')
@login_required
def logoutpage_page():
    """Summary or Description of the function

    Parameters:

    Returns:
    object: User
    None
    """

    if os.path.exists("ms_graph_api_token.json"):
        os.remove("ms_graph_api_token.json")
    else:
        pass
    return redirect(url_for('logout_method'))


@app.route('/logout_method')
def logout_method():
    """Summary or Description of the function

    Parameters:

    Returns:
    object: User
    None
    """

    logout_user()
    return render_template("logoutpage.html")


@app.route('/onedrive')
@login_required
def onedrive():
    """Summary or Description of the function

    Parameters:

    Returns:
    object: User
    None
    """
    app_id = '5e84b5a7-fd04-4398-a15f-377e3d85703e'
    scopes = ['Files.ReadWrite']
    # global ACCESS_TOKEN
    access_token = generate_access_token(app_id, scopes)
    headers = {
        'Authorization': 'Bearer ' + access_token['access_token']
    }
    return headers


def check_for_duplicate_group(group_name):
    """Summary or Description of the function

    Parameters:

    Returns:
    object: User
    None
    """

    connection = sqlite3.connect("group.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT group_name FROM groups WHERE group_name = ?",
        (group_name,))
    existing_group = cursor.fetchone()
    connection.close()
    return existing_group is not None


@app.route('/form_create_group', methods=['POST'])
def create_group():
    """Summary or Description of the function

    Parameters:

    Returns:
    object: User
    None
    """

    # Get form data
    group_name = request.form['group_name']

    # Check for duplicate group name
    if check_for_duplicate_group(group_name):
        error_message = "Create the group with a different name"
        return render_template(
            "create_group.html", error_message=error_message)
    # If group name is unique, continue with group creation logic
    # Your group creation logic here
    return "Group successfully created"


@app.route('/filefinder')
@login_required
def filefinder():
    """Summary or Description of the function

    Parameters:

    Returns:
    object: User
    None
    """
    url = 'https://graph.microsoft.com/v1.0/'
    headers = onedrive()
    file_list = ''
    timeout = 30
    items = json.loads(requests.get(url + 'me/drive/root/children',
                                    headers=headers, timeout=timeout).text)
    items = items['value']
    #  for entries in range(len(items)):

    for _, entry in enumerate(items):
        # get folders
        print(entry['name'], '| item-id >', entry['id'])
        file_list += "\n" + str(entry['name']) + "\n"
        current_folder = entry['id']
        # get files
        new_url = url + 'me/drive/items/' + current_folder + '/children'
        sub_items = json.loads(requests.get(new_url, headers=headers, timeout=timeout).text)
        sub_items = sub_items['value']
        #  for sub_entries in range(len(sub_items)):
        for _, sub_entry in enumerate(sub_items):
            print(sub_entry['name'], '| item-id >', sub_entry['id'])
            file_list += "\n" + '\t' + "- " + sub_entry['name'] + '\n'
    print(file_list)
    return render_template("fileexplorer.html", folders=file_list)


# if __name__ == "__main__":
#    app.run(debug=True)


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
    checkdatabase()
    login()
