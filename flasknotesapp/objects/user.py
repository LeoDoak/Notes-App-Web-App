"Image library, need to 'pip install Pillow'"
from PIL import Image
class User:
    user_id: str
    username: str
    password: str
    email: str
    profile_picture: Image
    priv_groups: list
    public_groups: list

    def __init__(self, user_id: str, username: str, password: str, email: str):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email

    def get_id(self):
        return str(self.user_id)

    def is_active(self):
        return True

    def is_authenticated(self):
        if self.username == username and self.password == password :
            return True 
        else:
            return False



    # sample list
SAMPLE_USERS = [
        User("1", "JohnSmith1", "Random12", "js7456@uncw.edu"),
        User("2", "AliceBarnes", "Password10", "ab1234@uncw.edu"),
        User("3", "BobbyHill123", "Qwerty123", "bh4201@uncw.edu"),
        User("4", "JettHoward", "Random12", "jh4321@uncw.edu"),
        User("0", "Admin", "1234", "admin@uncw.edu") #admin access
    ]
