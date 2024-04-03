"Image library, need to 'pip install Pillow'"
from PIL import Image
import sqlite3


class User():

    user_id: str
    username: str
    password: str
    email: str
    profile_picture: Image
    priv_groups: list
    public_groups: list
    access_token = ""

    def __init__(self, user_id: str, username: str, password: str, email: str):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email

    def toString(self):
        String = (
            "User ID: " + str(self.user_id) + " Username: " + 
            str(self.username) + " Password: " + str(self.password) + 
            " email: " + str(self.email))
        return String

    def get_id(self):
        return str(self.user_id)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def set_access_token(self, ac):
        self.access_token = ac

    def get_access_token(self):
        return self.access_token

    def is_authenticated(self):
        connection = sqlite3.connect("user.db")
        cursor = connection.cursor()
        cursor.execute(
            """SELECT user_id, username, password, 
            email FROM user where (username = ? and password = ?)""", 
            (self.username, self.password))
        row = cursor.fetchall()
        connection.close()
        return len(row) == 1

    def get_user_from_id(self, user_id):
        connection = sqlite3.connect("user.db")
        cursor = connection.cursor()
        cursor.execute(
            """SELECT user_id, username, password, 
            email FROM user where (user_id = ?)""",
            (user_id,))
        row = cursor.fetchall()
        connection.close()
        self.user_id = row[0][0]
        self.username = row[0][1]
        self.password = row[0][2]
        self.email = row[0][3]
        # return user

    def set_login_userID(self):
        connection = sqlite3.connect("user.db")
        cursor = connection.cursor()
        cursor.execute(
            "SELECT user_id FROM user where (username = ? and password = ?)",
            (self.username, self.password))
        row = cursor.fetchall()
        if len(row) == 1:
            self.user_id = row[0][0]
        else:
            self.user_id = None

    def set_login_email(self):
        connection = sqlite3.connect("user.db")
        cursor = connection.cursor()
        cursor.execute(
            "SELECT email FROM user where (username = ? and password = ?)",
            (self.username, self.password))
        row = cursor.fetchall()
        if len(row) == 1:
            self.email = row[0][0]
        else:
            self.email = None


    # sample list
SAMPLE_USERS = [
        User("1", "JohnSmith1", "Random12", "js7456@uncw.edu"),
        User("2", "AliceBarnes", "Password10", "ab1234@uncw.edu"),
        User("3", "BobbyHill123", "Qwerty123", "bh4201@uncw.edu"),
        User("4", "JettHoward", "Random12", "jh4321@uncw.edu"),
        User("0", "Admin", "1234", "admin@uncw.edu")  # admin access
    ]
