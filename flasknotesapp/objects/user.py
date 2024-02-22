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
SAMPLE_USERS = [
        User("1", "JohnSmith1", "Random12", "js7456@uncw.edu", None),
        User("2", "AliceBarnes", "Password10", "ab1234@uncw.edu", None),
        User("3", "BobbyHill123", "Qwerty123", "bh4201@uncw.edu", None),
        User("4", "JettHoward", "Random12", "jh4321@uncw.edu", None),
    ]