class User:
    user_id: str
    username: str
    password: str
    email: str
    #private group list
    #public group list
    #profile picture

    def __init__(self, user_id: str, username: str, password: str, email: str):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email

    # sample list