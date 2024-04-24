""" Main Server Page  """

import os
import sqlite3
import json
import flask
import requests
from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    session,
    make_response,
)
from flask_login import login_required, login_user, logout_user, LoginManager
from flask_wtf import FlaskForm
from waitress import serve
from wtforms import FileField, SubmitField
from databases import user_database
from objects.onedrive import generate_access_token, GRAPH_API_ENDPOINT
from objects.user import User
from objects.file_classes import File

# Don't know if we need 2 of these.

# Used this tutorial to figure out login screen
# https://www.youtube.com/watch?v=R-hkzqjRMwM&ab_channel=NachiketaHebbar

# used this for the sql request for placeholders,
# https://medium.com/@miguel.amezola/protecting-your-code-from-sql-injection-attacks-when-using-raw-sql-in-python-916466961c97
app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
app.config["UPLOAD_FOLDER"] = "static\\files"
app.secret_key = """967b75c111e64965848a7786bda9602
        f9d208f991036ccc4f793a4199a9f74b4"""

# ACCESS_TOKEN = ""  "Global variable that flake8 does not like"

login_manager = LoginManager()
login_manager.init_app(app)


def create_folder(headers, folder_name):
    """
    Creates a new folder on a user's OneDrive via the Microsoft Graph API,
    using an access token for authentication. Posts a request with the desired folder name,
    handles errors, and returns the API's response.

    Args:
        token: The access token for authentication.
        folder_name: The name of the folder to be created.

    Returns:
        The response from the OneDrive API as a JSON object.
    """
    url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
    json_headers = request.cookies.get(session["username"])
    headers = json.loads(json_headers)
    if headers is None:
        return render_template("homepage.html")

    response = requests.post(
        url, headers=headers, json={"name": folder_name, "folder": {}}, timeout=10
    )
    response.raise_for_status()
    return response.json()


def copy_file_to_favorites(headers, file_id, favorites_folder_id):
    """
    copy a file to the 'Favorites' folder in OneDrive.

    :param headers: Authorization headers.
    :param file_id: ID of the file to move.
    :param favorites_folder_id: ID of the 'Favorites' folder.
    :return: JSON response from the OneDrive API.
    """
    copy_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/copy"
    body = {
        "parentReference": {
            "id": favorites_folder_id
        }
    }
    response = requests.post(copy_url, headers=headers, json=body, timeout=30)
    response.raise_for_status()


def copy_file_to_favorites_shared(headers, file_id, favorites_folder_id):
    """
    copy a file to the 'Favorites' folder in OneDrive from a shared folder.

    :param headers: Authorization headers.
    :param file_id: ID of the file to move.
    :param favorites_folder_id: ID of the 'Favorites' folder.
    :return: JSON response from the OneDrive API.
    """
    ids_split = file_id.split(",")
    driveid = ids_split[1]
    fileid = ids_split[0]
    # /drives/{driveId}/items/{itemId}/copy
    # copy_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/copy"
    copy_url = f"https://graph.microsoft.com/v1.0/drives/{driveid}/items/{fileid}/copy"
    body = {
        "parentReference": {
            "id": favorites_folder_id
        }
    }
    response = requests.post(copy_url, headers=headers, json=body, timeout=30)
    print(response)
    response.raise_for_status()


@login_manager.user_loader
def load_user(user_id):
    """Load a user object from the database given its user ID.

    Parameters:
    user_id (int): the User_ID given to each of the users.

    Returns:
    User or None: User object which is the same user with that ID.
    None: object doesn't exist.
    """

    connection = sqlite3.connect("user.db")
    cursor = connection.cursor()
    cursor.execute(
        """SELECT user_id, username, password,
        email FROM user where (user_id = ?)""",
        (user_id,),
    )
    row = cursor.fetchall()
    print(row, "\n")
    connection.close()
    if len(row) == 1:
        return User(row[0][0], row[0][1], row[0][2], row[0][3])
    return None


def checkdatabase():
    """calls the function that creates the database from the user_database file.

    Parameters:
    None.

    Returns:
    None.
    """
    # call the function that creates the database
    user_database.create_database()


@app.route("/")
def set_up():
    """Sets up the loginpage to set up the flask project.

    Parameters:
    None.

    Returns:
    flask method: render_template with String loginpage.html.
    """

    return render_template("loginpage.html")


@app.route("/form_login", methods=["POST", "GET"])
def login():
    """Handles the user login functionality.

    Parameters:
    None.

    Returns:
    flask method: that redirects to homepage or render_template
    with loginpage.html and the errors messages with it.
    """

    get_name = request.form["username"]
    get_password = request.form["password"]
    current_user = User(None, get_name, get_password, None)
    if current_user.is_authenticated():
        flask.flash("Logged in successfully.")
        current_user.set_login_user_id()
        current_user.set_login_email()
        login_user(current_user)
        # next = flask.request.args.get('next')
        session["username"] = (
            get_name  # set the session key for getting the One Drive header
        )
        return redirect(url_for("homepage"))
    error_message = "Incorrect Username or Password!"
    return render_template("loginpage.html", msg=error_message)


@app.route("/homepage")
@login_required
def homepage():
    """Loads the homepage.

    Parameters:
    None.

    Returns:
    Flask method with homepage.html.
    """

    return render_template("homepage.html")


@app.route("/register")
def register():
    """Loads the register page.

    Parameters:
    None.

    Returns:
    flask method that has the register.html page.
    """

    return render_template("register.html")


@app.route("/form_register", methods=["POST", "GET"])
def register_actions():
    """Handles the register form and adds the user to database.

    Parameters:
    None.

    Returns:
    flask method with register.html with the error messages or
    flask method with homepage.html.
    """
    get_email = request.form["email"]
    get_name = request.form["username"]
    get_password = request.form["password"]
    get_confirmpassword = request.form["confirmpassword"]

    # create new user
    new_user = User(None, get_name, get_password, get_email)

    # check user
    (
        username_message,
        email_message,
        password_message,
        confirm_password_message,
        register_status,
    ) = new_user.check_new_user(get_confirmpassword)

    if register_status is False:
        print("not able to regster")
        return render_template(
            "register.html",
            email_error=email_message,
            username_error=username_message,
            password_error=password_message,
            confirm_password_error=confirm_password_message,
        )
    print("registered")
    flask.flash("Logged in successfully.")
    login_user(new_user)
    return render_template("homepage.html")


@app.route("/forgotpsd")
def forgot_password():
    """Function that loads the forgot password page.

    Parameters:
    None.

    Returns:
    Flask method that has the 'forgot_pswd.html' page.
    """

    return render_template("forgot_pswd.html")


class UploadFileForm(FlaskForm):
    """Summary or Description of the function
    Gives the file that is uploaded
    Parameters: specified formdata

    Returns: uploaded file
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


@app.route("/upload", methods=["POST"])
@login_required
def upload_page_setup():
    """Uploads a file to OneDrive"""
    group = request.form["title"]
    form = UploadFileForm()
    return render_template("upload.html", form=form, group=group)


@app.route("/upload_page_action", methods=["GET", "POST"])
@login_required
def upload_page_action():
    """Summary:"""
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    group = request.form["group"]
    #  Use request.files to access uploaded files (chatgpt helped get the files part)
    file = request.files["file"]
    timeout = 60
    print(group, file.filename)
    if file:
        response = requests.put(
            GRAPH_API_ENDPOINT
            + f"/me/drive/items/root:/{group}/{file.filename}:/content",
            headers=headers,
            data=file.read(),  # Use file.read() to get the file content
            timeout=timeout,
        )
        print(response.json())

    return get_my_folders()


@app.route("/upload_page_setup_shared", methods=["POST"])
@login_required
def upload_page_setup_shared():
    """Uploads a file to OneDrive"""
    group = request.form["title"]
    file_id = request.form["file_id"]
    form = UploadFileForm()
    return render_template(
        "upload_shared.html", form=form, group=group, file_id=file_id
    )


@app.route("/upload_page_action_shared", methods=["GET", "POST"])
@login_required
def upload_page_action_shared():
    """Summary:"""
    url = "https://graph.microsoft.com/v1.0/"
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    group = request.form["group"]
    current_folder_ids = request.form["file_id"]
    ids_split = current_folder_ids.split(",")
    drive_id = ids_split[0]
    remote_id = ids_split[1]
    #  Use request.files to access uploaded files (chatgpt helped get the files part)
    file = request.files["file"]
    timeout = 60
    print(group, file.filename)
    new_url = f"/drives/{drive_id}/items/{remote_id}:/{file.filename}:/content"
    print(new_url)
    if file:
        response = requests.put(
            url + new_url,
            headers=headers,
            data=file.read(),  # Use file.read() to get the file content
            timeout=timeout,
        )
        print(response.json())

    return get_shared_folders()


@app.route("/group")
@login_required
def group_page():
    """Render the group page.

    This function renders the 'groups.html' template, which represents the group creation page.

    Returns:
    rendered_template: HTML content of the rendered template.
    """

    return render_template("groups.html")


@app.route("/group_details")
@login_required
def group_details_page():
    """
    Render the group details page.

    This function retrieves the value of the 'title' query parameter from the request.
    If the parameter is not provided, it defaults to 'Default Group Name'.
    The function then renders the 'group_details.html' template, passing the retrieved group name.

    Returns:
    rendered_template: HTML content of the rendered template.
    """
    group_name = request.args.get("title", "Default Group Name")
    return render_template("group_details.html", group_name=group_name)


@app.route("/logout")
@login_required
def logoutpage_page():
    """Summary or Description of the function

    Parameters:

    Returns:
    """

    if os.path.exists("ms_graph_api_token.json"):
        os.remove("ms_graph_api_token.json")
    else:
        pass
    return redirect(url_for("logout_method"))


@app.route("/logout_method")
def logout_method():
    """Summary or Description of the function

    Parameters:

    Returns:
    object: User
    None.
    """

    logout_user()
    return render_template("logoutpage.html")


@app.route("/onedrive")
@login_required
def onedrive():
    """Summary or Description of the function
    Authenticates with onedrive account
    Parameters:
    None
    Returns: headers to access onedrive account
    object: User
    None
    """
    app_id = "5e84b5a7-fd04-4398-a15f-377e3d85703e"
    scopes = ["Files.ReadWrite"]
    access_token = generate_access_token(app_id, scopes)
    headers = {"Authorization": "Bearer " + access_token["access_token"]}
    resp = make_response("One Drive login opening in another page")
    json_headers = json.dumps(headers, indent=4)
    resp.set_cookie(session["username"], json_headers)  # setting the session ID
    print("Cookie is set")
    return resp


def check_for_duplicate_group(group_name):
    """Check for the existence of a group with the given name in the database.

    This function connects to the 'group.db' SQLite database and executes a query to select
    a group with the provided group_name from the 'groups' table. If a group with the given
    name exists, it returns the group; otherwise, it returns None.

    Parameters:
    group_name (str): The name of the group to check for duplicates.

    Returns:
    object: The existing group if found, None otherwise.
    """

    connection = sqlite3.connect("group.db")
    cursor = connection.cursor()
    cursor.execute("SELECT group_name FROM groups WHERE group_name = ?", (group_name,))
    existing_group = cursor.fetchone()
    connection.close()
    return existing_group is not None


@app.route("/create_group", methods=["POST"])
def create_group():
    """Summary: Creates a seperate folder with the title of the group in onedrive.
    Params:
    Returns:
    """
    group_name = request.form.get("group_name")

    # Retrieve authentication headers
    url = "https://graph.microsoft.com/v1.0/"
    json_headers = request.cookies.get(session["username"])

    if json_headers is None:
        return jsonify({"error": "Authentication headers not found"}), 401

    headers = json.loads(json_headers)

    # Create folder in OneDrive
    create_url = url + "/me/drive/root/children"
    body = {
        "name": group_name,
        "folder": {},
        "@microsoft.graph.conflictBehavior": "rename",
    }

    try:
        response = requests.post(create_url, headers=headers, json=body, timeout=30)
        response.raise_for_status()  # Raise an error for non-2xx status codes
        return (
            render_template("groups.html", message="Folder created successfully"),
            200,
        )
    except requests.exceptions.RequestException as e:
        return (
            render_template(
                "groups.html",
                error=f"Failed to create group folder in OneDrive: {str(e)}",
            ),
            500,
        )


@app.route("/get_main_folders")
def get_main_folders():
    """Summary: Gets the shared and personal folders, displays them.
    Params:
    Returns:
    """
    shared_folder = File(None, "Shared With Me", None, None)
    shared_folder.set_filetype()
    shared_folder.set_file_icon()
    my_folder = File(None, "My Files", None, None)
    my_folder.set_filetype()
    my_folder.set_file_icon()

    return render_template(
        "main_folder.html", shared_folder=shared_folder, my_folder=my_folder
    )


@app.route("/get_shared_folders")
def get_shared_folders():
    """Function that lists the files in a User's onedrive.

    Parameters:
    None.

    Returns:
    flask method with the filexplorer.html page with the OneDrive files.
    """
    url = "https://graph.microsoft.com/v1.0/"
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    file_list = []
    timeout = 30
    items = json.loads(
        requests.get(
            url + "/me/drive/sharedWithMe", headers=headers, timeout=timeout
        ).text
    )
    items = items["value"]
    print(items)
    #  for entries in range(len(items)):
    for _, entry in enumerate(items):
        # get folders
        remote_item = entry["remoteItem"]
        parent_ref = remote_item["parentReference"]
        print(entry["name"], "| item-id >", parent_ref["driveId"])
        id_linked = parent_ref["driveId"] + "," + remote_item["id"]
        new_file = File(id_linked, entry["name"], None, None)
        new_file.set_filetype()
        new_file.set_file_icon()
        print(new_file.get_filetype())
        if "folder" in new_file.get_filetype():
            file_list.append(new_file)
    print(file_list)
    return render_template("shared_file_groups.html", folders=file_list)


@app.route("/get_my_folders")
def get_my_folders():
    """Function that lists the files in a User's onedrive.

    Parameters:
    None.

    Returns:
    flask method with the filexplorer.html page with the OneDrive files.
    """
    url = "https://graph.microsoft.com/v1.0/"
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    file_list = []
    timeout = 30
    items = json.loads(
        requests.get(
            url + "me/drive/root/children", headers=headers, timeout=timeout
        ).text
    )
    items = items["value"]
    #  for entries in range(len(items)):
    for _, entry in enumerate(items):
        # get folders
        print(entry["name"], "| item-id >", entry["id"])
        new_file = File(entry["id"], entry["name"], None, None)
        new_file.set_filetype()
        new_file.set_file_icon()
        print(new_file.get_filetype())
        if "folder" in new_file.get_filetype():
            file_list.append(new_file)
    print(file_list)
    return render_template("file_groups.html", folders=file_list)


@app.route("/get_my_personal_files", methods=["POST"])
def get_my_personal_files():
    """Summary
    Params:
    Returns:
    """
    timeout = 30
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    file_list = []
    url = "https://graph.microsoft.com/v1.0/"
    #  sget from other flask method
    current_folder = request.form["file_id"]
    #  print("Current folder Id:", current_folder)
    new_url = url + "me/drive/items/" + current_folder + "/children"
    sub_items = json.loads(requests.get(new_url, headers=headers, timeout=timeout).text)
    #  print(sub_items)
    sub_items = sub_items["value"]
    #  for sub_entries in range(len(sub_items)):
    for _, sub_entry in enumerate(sub_items):
        #  print(sub_entry['name'], '| item-id >', sub_entry['id'])
        new_file = File(sub_entry["id"], sub_entry["name"], None, None)
        # setting the filetype from the name
        new_file.set_filetype()
        # indexing the photo from filetype
        new_file.set_file_icon()
        file_list.append(new_file)
        #  print(new_file.get_title(),new_file.get_filetype(),"\n")
    return render_template("fileexplorer.html", folders=file_list)


@app.route("/get_my_shared_files", methods=["POST"])
def get_my_shared_files():
    """Summary
    Params:
    Returns:
    """
    timeout = 30
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    file_list = []
    url = "https://graph.microsoft.com/v1.0/"
    #  sget from other flask method
    current_folder_ids = request.form["file_id"]
    ids_split = current_folder_ids.split(",")
    print(ids_split)
    drive_id = ids_split[0]
    remote_id = ids_split[1]
    new_url = url + "drives/" + drive_id + "/items/" + remote_id + "/children"
    sub_items = json.loads(requests.get(new_url, headers=headers, timeout=timeout).text)
    sub_items = sub_items["value"]
    #  for sub_entries in range(len(sub_items)):
    for _, sub_entry in enumerate(sub_items):
        #  print(sub_entry['name'], '| item-id >', sub_entry['id'])
        id_field = sub_entry["id"] + "," + drive_id
        new_file = File(id_field, sub_entry["name"], None, None)
        # setting the filetype from the name
        new_file.set_filetype()
        # indexing the photo from filetype
        new_file.set_file_icon()
        file_list.append(new_file)
        #  print(new_file.get_title(),new_file.get_filetype(),"\n")
    return render_template("fileexplorer_shared.html", folders=file_list)


@app.route("/delete_file", methods=["POST"])
@login_required
def delete_file():
    """Summary:
    Params:
    Returns:
    """
    timeout = 30
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    file_id = request.form["file_id"]
    file_name = request.form["file_title"]
    m_url = "https://graph.microsoft.com/v1.0/"
    url = "/me/drive/items/" + file_id
    url = m_url + url
    response = requests.delete(url, headers=headers, timeout=timeout)
    if response.status_code == 204:
        message = "Item gone! If need to recover, please check OneDrive Recycle Bin."
    else:
        message = "Item could not be deleted. Go back and try again"
    return render_template("deleted_file.html", title=file_name, message=message)


@app.route("/download_file", methods=["POST"])
@login_required
def download_file():
    """Summary: Downloading files from One Drive
    Params:
    Returns:
    Credit:
    """
    timeout = 30
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    m_url = "https://graph.microsoft.com/v1.0/"
    file_id = request.form["file_id"]
    file_title = request.form["file_title"]
    url = "me/drive/items/" + file_id + "/content"
    url = m_url + url
    file_name = file_title
    save_location = os.path.expanduser("~/Downloads")
    response_file_contenet = requests.get(url, headers=headers, timeout=timeout)
    with open(os.path.join(save_location, file_name), "wb") as _f:
        _f.write(response_file_contenet.content)
    return render_template("download_file.html", title=file_name)

    @app.route("/download_file_shared", methods=["POST"])
    @login_required
    def download_file_shared():
        """Summary: Downloading files from One Drive
        Params:
        Returns:
        Credit:
        """
        timeout = 30
        json_headers = request.cookies.get(session["username"])
        if json_headers is None:
            return render_template("homepage.html")
        headers = json.loads(json_headers)
        m_url = "https://graph.microsoft.com/v1.0/"
        file_id = request.form["file_id"]
        file_id = file_id.split(',')[0]
        file_title = request.form["file_title"]
        url = "me/drive/items/" + file_id + "/content"
        url = m_url + url
        file_name = file_title
        save_location = os.path.expanduser("~/Downloads")
        response_file_contenet = requests.get(url, headers=headers, timeout=timeout)
        with open(os.path.join(save_location, file_name), "wb") as _f:
            _f.write(response_file_contenet.content)
        return render_template("download_file.html", title=file_name)


@app.route("/get_favorites", methods=["GET", "POST"])
def get_favorites():
    '''this function helps to display files in fav_tab
    '''
    timeout = 30
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    file_list = []
    url = "https://graph.microsoft.com/v1.0/"
    #  sget from other flask method
    current_folder = get_or_create_favorites_folder(headers)
    new_url = url + "me/drive/items/" + current_folder + "/children"
    sub_items = json.loads(requests.get(new_url, headers=headers, timeout=timeout).text)
    sub_items = sub_items["value"]
    #  for sub_entries in range(len(sub_items)):
    for _, sub_entry in enumerate(sub_items):
        new_file = File(sub_entry["id"], sub_entry["name"], None, None)
        # setting the filetype from the name
        new_file.set_filetype()
        # indexing the photo from filetype
        new_file.set_file_icon()
        file_list.append(new_file)
    return render_template("favoriteexplorer.html", folders=file_list)


@app.route("/add_favorite", methods=["POST"])
def add_favorite():
    """ move file to favorites folder
    """
    timeout = 30
    json_headers = request.cookies.get(session["username"])
    print("jason", json_headers)
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    file_id = request.form["file_id"]
    # file_name = request.form["file_title"]
    m_url = "https://graph.microsoft.com/v1.0/"
    url = "/me/drive/items/" + file_id
    url = m_url + url
    print("url id:", url)
    # if folder favorite does not exist, create it
    favorites_folder_id = get_or_create_favorites_folder(headers)
    print("Favorites ID", favorites_folder_id)
    # move file to favorites folder
    # token = headers["Authorization"]
    copy_file_to_favorites(headers, file_id, favorites_folder_id)
    return get_favorites()


@app.route("/add_favorite_shared", methods=["POST"])
def add_favorite_shared():
    """ move file to favorites folder
    """
    timeout = 30
    json_headers = request.cookies.get(session["username"])
    print("jason", json_headers)
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    file_id = request.form["file_id"]
    # file_name = request.form["file_title"]
    m_url = "https://graph.microsoft.com/v1.0/"
    url = "/me/drive/items/" + file_id
    url = m_url + url
    print("url id:", url)
    # if folder favorite does not exist, create it
    favorites_folder_id = get_or_create_favorites_folder(headers)
    print("Favorites ID", favorites_folder_id)
    # move file to favorites folder
    # token = headers["Authorization"]
    copy_file_to_favorites_shared(headers, file_id, favorites_folder_id)
    return get_favorites()


def get_or_create_favorites_folder(headers):
    '''
    Summary:
    '''
    search_url = "https://graph.microsoft.com/v1.0/me/drive/root/children"

    # Send a request to retrieve the folders
    response = requests.get(search_url, headers=headers, timeout=30)

    # Check if the request was successful
    if response.status_code == 200:
        # Search for the 'Notes-App{Favorites}' folder
        folders = response.json()['value']
        for folder in folders:
            if folder.get('name') == 'Notes-App{Favorites}' and 'folder' in folder:
                return folder['id']

        # If the folder doesn't exist, create it
        create_folder_url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
        payload = {
            "name": "Notes-App{Favorites}",
            "folder": {}
        }
        create_response = requests.post(create_folder_url, headers=headers, json=payload)

        if create_response.status_code == 201:
            return create_response.json().get('id')
        else:
            print("Error creating 'Notes-App{Favorites}' folder:", create_response.json())
            create_response.raise_for_status()
    else:
        print("Error searching for 'Notes-App{Favorites}' folder:", response.json())
        response.raise_for_status()
    return None


@app.route("/searchfiles", methods=["POST"])
@login_required
def searchfiles():
    """Summary: Search Files
    Params:
    Returns:
    """
    search_criteria = request.form["Search"]
    url = "https://graph.microsoft.com/v1.0/"
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    file_list = []
    timeout = 30
    items = json.loads(
        requests.get(
            url + "me/drive/root/children", headers=headers, timeout=timeout
        ).text
    )
    items = items["value"]
    #  for entries in range(len(items)):
    for _, entry in enumerate(items):
        # get folders
        #  print(entry['name'], '| item-id >', entry['id'])
        new_file = File(entry["id"], entry["name"], None, None)
        new_file.set_filetype()
        new_file.set_file_icon()
        if search_criteria.lower() in entry["name"]:
            file_list.append(new_file)
        current_folder = entry["id"]
        # get files
        new_url = url + "me/drive/items/" + current_folder + "/children"
        sub_items = json.loads(
            requests.get(new_url, headers=headers, timeout=timeout).text
        )
        sub_items = sub_items["value"]
        #  for sub_entries in range(len(sub_items)):
        for _, sub_entry in enumerate(sub_items):
            #  print(sub_entry['name'], '| item-id >', sub_entry['id'])
            new_file = File(sub_entry["id"], sub_entry["name"], None, None)
            new_file.set_filetype()
            #  setting the filetype from the name
            new_file.set_file_icon()
            #  indexing the photo from filetype
            if search_criteria.lower() in sub_entry["name"]:
                file_list.append(new_file)
            #  print(new_file.get_title(),new_file.get_filetype(),"\n")
    return render_template("searchtemplate.html", folders=file_list)


@app.route("/share_my_group", methods=["POST"])
@login_required
def share_group_setup():
    """Sumary: sets up for sharing personal file"""
    file_id = request.form["file_id"]
    title = request.form["title"]
    return render_template("share_group_setup.html", file_id=file_id, title=title)


@app.route("/share_group_action", methods=["POST"])
@login_required
def share_group_action():
    """Summary: Share personal group with someone"""
    timeout = 30
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    #  shoutout chatgpt if this works
    email = request.form["email"]
    folder_id = request.form["file_id"]
    title = request.form["title"]
    share_data = {
        "recipients": [{"email": email}],
        "requireSignIn": True,
        "sendInvitation": True,
        "roles": ["write"],
    }
    share_response = requests.post(
        f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}/invite",
        headers=headers,
        json=share_data,
        timeout=timeout,
    )
    if share_response == 400:
        print("error")
    return render_template("share_group_setup.html", file_id=folder_id, title=title)


@app.route("/share_my_group_shared", methods=["POST"])
@login_required
def share_group_setup_shared():
    """Sumary: sets up for sharing shared group"""
    file_id = request.form["file_id"]
    title = request.form["title"]
    return render_template(
        "shared_group_setup_shared.html", file_id=file_id, title=title
    )


@app.route("/share_group_action_shared", methods=["POST"])
@login_required
def share_group_action_shared():
    """Summary: Share shared group with someone"""
    timeout = 60
    url = "https://graph.microsoft.com/v1.0/"
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    #  shoutout chatgpt if this works
    email = request.form["email"]
    folder_id = request.form["file_id"]
    current_folder_ids = request.form["file_id"]
    ids_split = current_folder_ids.split(",")
    drive_id = ids_split[0]
    remote_id = ids_split[1]
    new_url = url + "drives/" + drive_id + "/items/" + remote_id + "/invite"
    title = request.form["title"]
    share_data = {
        "recipients": [{"email": email}],
        "requireSignIn": True,
        "sendInvitation": True,
        "roles": ["write"],
    }
    share_response = requests.post(
        new_url, headers=headers, json=share_data, timeout=timeout
    )
    if share_response == 400:
        print("error")
    return render_template(
        "shared_group_setup_shared.html", file_id=folder_id, title=title
    )


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
    checkdatabase()
    login()
