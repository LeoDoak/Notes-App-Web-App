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

    # sample list