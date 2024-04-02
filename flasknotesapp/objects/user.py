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
    access_token = ""

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

    def set_access_token(self, ac):
        self.access_token = ac

    def get_access_token(self):
        return self.access_token
