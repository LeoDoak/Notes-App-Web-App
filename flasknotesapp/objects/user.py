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

    def __init__(self, user_id: str, username: str, password: str, email: str, profile_picture: Image):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.profile_picture = profile_picture

    # sample list