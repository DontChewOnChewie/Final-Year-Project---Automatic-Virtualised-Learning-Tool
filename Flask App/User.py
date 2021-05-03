'''
Class used as model for a User.
'''
class User:

    # Constructor for User object.
    def __init__(self, id, username, email, password, sign_up_date, last_login, failed_login_count, locked):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.sign_up_date = sign_up_date
        self.last_login = last_login
        self.failed_login_count = failed_login_count
        self.locked = locked