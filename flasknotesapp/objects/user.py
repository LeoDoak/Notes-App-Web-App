"Image library, need to 'pip install Pillow'"
from PIL import Image
import sqlite3
class User:
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
        print(type(self.user_id))
        print(type(self.username))
        print(type(self.password))
        print(type(self.email))
        String = ("User ID: " + str(self.user_id)+ " Username: " + self.username + " Password: " + self.password + " email: " + self.email )
        return String

    def get_id(self):
        return str(self.user_id)

    def is_active(self):
        return True

    def is_authenticated(self):
        if self.username == username and self.password == password :
            return True 
        else:
            return False

    def set_access_token(self, ac):
        self.access_token = ac

    def get_access_token(self):
        return self.access_token

    def check_login(self, test_username, test_password):
        connection = sqlite3.connect("user.db")
        cursor =  connection.cursor()
        cursor.execute("SELECT user_id, username, password, email  FROM user where (username = ? and password = ?)",(test_username, test_password))
        row = cursor.fetchall()
        print("row:", row)
        connection.close()
        if len(row) == 1: 
            if row[0][1] == test_username and row[0][2] == test_password:
                self.username = test_username # set username 
                self.password = test_password # set password
                self.set_login_userID() #update user instance with user_id
                self.set_login_email() #update user instance with email
                return True 
            else: 
                return False
        else:
            return False

    def set_login_userID(self):
        connection = sqlite3.connect("user.db")
        cursor =  connection.cursor()
        cursor.execute("SELECT user_id FROM user where (username = ? and password = ?)",(self.username, self.password))
        row = cursor.fetchall()
        self.user_id = row[0][0]

    def set_login_email(self):
        connection = sqlite3.connect("user.db")
        cursor =  connection.cursor()
        cursor.execute("SELECT email FROM user where (username = ? and password = ?)",(self.username, self.password))
        row = cursor.fetchall()
        print(row)
        self.email = row[0][0]




        
      
        

    # sample list
SAMPLE_USERS = [
        User("1", "JohnSmith1", "Random12", "js7456@uncw.edu"),
        User("2", "AliceBarnes", "Password10", "ab1234@uncw.edu"),
        User("3", "BobbyHill123", "Qwerty123", "bh4201@uncw.edu"),
        User("4", "JettHoward", "Random12", "jh4321@uncw.edu"),
        User("0", "Admin", "1234", "admin@uncw.edu") #admin access
    ]