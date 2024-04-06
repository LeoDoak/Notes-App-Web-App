"Image library, need to 'pip install Pillow'"
import sqlite3
import re
from PIL import Image
import numpy as np


# https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/


class User():
    """Summary or Description of the function

    Parameters:

    Returns:
    """
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

    def __str__(self):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        string = (
                "User ID: " + str(self.user_id) + " Username: " +
                str(self.username) + " Password: " + str(self.password) +
                " email: " + str(self.email))
        return string

    def get_id(self):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        return str(self.user_id)

    def is_active(self):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        return True

    def is_anonymous(self):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        return False

    def set_access_token(self, ac):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        self.access_token = ac

    def get_access_token(self):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        return self.access_token

    def is_authenticated(self):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
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
        """Summary or Description of the function

        Parameters:

        Returns:
        """
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

    def set_login_user_id(self):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
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
        """Summary or Description of the function

        Parameters:

        Returns:
        """
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

    def _check_valid_username(self):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        pattern = r'^(?=.*[a-zA-Z].*[a-zA-Z].*[a-zA-Z].*[a-zA-Z]).{5,}$'
        if re.match(pattern, self.username):
            return ''
        return 'Username does not meet criteria'

    def _check_duplicate_username(self):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        connection = sqlite3.connect("user.db")
        cursor = connection.cursor()
        cursor.execute(
            "SELECT username FROM user where username = ?", (self.username,))
        row = cursor.fetchall()
        connection.close()
        if len(row) == 1:
            return 'Username is already taken'
        return ''

    def _check_username(self):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        message = self._check_valid_username()
        if message == '':
            message = self._check_duplicate_username()
            return message
        return message

    def _check_valid_email(self):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.fullmatch(regex, self.email):
            return ''
        return "Invalid email entered"

    def _check_duplicate_email(self):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        connection = sqlite3.connect("user.db")
        cursor = connection.cursor()
        cursor.execute("SELECT email FROM user where email = ?", (self.email,))
        row = cursor.fetchall()
        connection.close()
        if len(row) == 1:
            return "Email already registered for account"
        return ''

    def _check_email(self):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        message = self._check_valid_email()
        if message == '':
            message = self._check_duplicate_email()
            return message
        return message

    def _validate_password(self):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        pattern = r'^(?=.*[0-9])(?=.*[^a-zA-Z0-9]).{9,}$'
        if re.match(pattern, self.password):
            return ""
        return "Password does not meet criteria"

    def _check_confirm_password(self, confirm_password):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        if self.password == confirm_password:
            return ''
        return 'Passwords do not match'

    def check_new_user(self, confirm_password):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        username_message = self._check_username()
        email_message = self._check_email()
        password_message = self._validate_password()
        confirm_password_message = self._check_confirm_password(confirm_password)
        register_status = False
        if (username_message == '' and
                email_message == '' and
                password_message == '' and
                confirm_password_message == ''):
            register_status = True
            self._set_user_id()
            self._update_database()
        return (
            username_message,
            email_message,
            password_message,
            confirm_password_message,
            register_status
        )

    def _set_user_id(self):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        id_num = np.random.randint(0, 99, 2)
        get_user_id = str(id_num[0]) + str(id_num[1])
        self.user_id = get_user_id

    def _update_database(self):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        connection = sqlite3.connect("user.db")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO user VALUES (?,? ,? ,?)",
            (self.user_id, self.username, self.password, self.email,))
        connection.commit()
        connection.close()


SAMPLE_USERS = [
    # Sample List
    User("1", "JohnSmith1", "Random12", "js7456@uncw.edu"),
    User("2", "AliceBarnes", "Password10", "ab1234@uncw.edu"),
    User("3", "BobbyHill123", "Qwerty123", "bh4201@uncw.edu"),
    User("4", "JettHoward", "Random12", "jh4321@uncw.edu"),
    User("0", "Admin", "1234", "admin@uncw.edu")  # admin access
]
