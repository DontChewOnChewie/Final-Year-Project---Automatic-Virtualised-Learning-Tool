import hashlib
import sqlite3
from datetime import datetime
from User import User
from string import ascii_letters
import random
from SessionDao import SessionDao

'''
Class used for managing data access to Account table of database.
Any autologin code is not yet 100% functional within the app and
will be a future development.
'''
class UserDao:

    # Constructor for UserDao object.
    # cursor = Existing database cursor.
    # db_name = Name of database file to connect to.
    def __init__(self, cursor=None, db_name="db.db"):
        self.db_name = db_name
        if not cursor:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
        else:
            self.cursor = cursor

    # Function used to hash a given password using SHA-512.
    def hash_password(self, password):
        return hashlib.sha512(password.encode('utf-8')).hexdigest()

    # Function used to check if an account with the same name and email already exists.
    def check_account_exists(self, credentials):
        self.cursor.execute("SELECT USERNAME, EMAIL \
                             FROM Account \
                             WHERE USERNAME = ? AND EMAIL = ?", (credentials[0], credentials[1]))
        record = self.cursor.fetchone()
        return True if record else False
    
    # Function used to get a users ID from there name and email.
    def get_user_id_from_name_and_email(self, username, email):
        self.cursor.execute("SELECT ID FROM Account \
                             WHERE USERNAME = ? AND EMAIL = ?", (username, email))
        record = self.cursor.fetchone()
        return record[0] if record else None
    
    # Function used to get a users ID from their name and session key.
    def get_user_id_from_name_and_session_key(self, username, session_key):
        self.cursor.execute("SELECT a.ID FROM Account a \
                             JOIN User_Session u ON a.ID = u.USER_ID \
                             WHERE a.USERNAME = ? AND u.SESSION_KEY = ?", (username, session_key))
        record = self.cursor.fetchone()
        return record[0] if record else None
    
    # Function used to get a User object from a users username.
    def get_user_from_username(self, username):
        self.cursor.execute("SELECT * FROM Account \
                             WHERE USERNAME = ?", (username,))
        record = self.cursor.fetchone()
        return User(*record) if record else None
    
    # Function used to update the users last login time.
    def update_last_login(self, user_id):
        timestamp = datetime.timestamp(datetime.now())
        self.cursor.execute("UPDATE Account \
                             SET LAST_SIGN_IN = ? \
                             WHERE ID = ?", (timestamp, user_id))
        self.conn.commit()

    # Function used to sign up a brand new users.
    def signup(self, credentials, ip, auto_login):
        try:
            timestamp = datetime.timestamp(datetime.now())
            self.cursor.execute("INSERT INTO Account (USERNAME, EMAIL, PASSWORD, SIGN_UP_DATE, LAST_SIGN_IN) \
                                VALUES (?, ?, ?, ?, ?)", (credentials[0], 
                                                        credentials[1],
                                                        self.hash_password(credentials[2]),
                                                        timestamp,
                                                        timestamp))
            user_id = self.get_user_id_from_name_and_email(credentials[0], credentials[1])
            user = User(user_id, credentials[0], credentials[1], credentials[2], timestamp, timestamp, 0, 0)
            sdao = SessionDao(self.cursor)
            key = sdao.update_session_key(user, ip)

            if auto_login:
                sdao.enable_auto_login(user.id, ip)
            self.conn.commit()
            sdao.close()
        except sqlite3.IntegrityError:
            return "Username {} is already taken, please try again.".format(credentials[0])

        return [user, key]

    # Function used to login an exisiting user.
    def login(self, credentials, ip, auto_login):
        self.cursor.execute("SELECT * FROM Account \
                            WHERE USERNAME = ? AND EMAIL = ? AND PASSWORD = ?", (credentials[0],
                                                                                 credentials[1],
                                                                                 self.hash_password(credentials[2])))
        record = self.cursor.fetchone()

        if record:
            user = User(*record)
            self.update_last_login(user.id)
            sdao = SessionDao(self.cursor)
            key = sdao.update_session_key(user, ip)
            if auto_login:
                sdao.enable_auto_login(user.id, ip)
            self.conn.commit()
            sdao.close()

        return [user, key] if record else "Password for account credentials inccorect"

    # Function used to attempt an auto login request with a username and key.
    def auto_login(self, username, key):
        self.cursor.execute("SELECT a.* FROM Account a \
                             JOIN User_Session u ON a.ID = u.USER_ID \
                             WHERE a.USERNAME = ? AND u.SESSION_KEY = ?", (username, key))
        record = self.cursor.fetchone()
        return User(*record) if record else None

    # Function used to validate a users session.
    # This function is called before any uploading or deleting from the server.
    def check_session_key(self, user, session_key):
        self.cursor.execute("SELECT a.ID FROM Account a \
                             JOIN User_Session u ON a.ID = u.USER_ID \
                             WHERE a.USERNAME = ? AND u.SESSION_KEY = ?", (user, session_key))
        record = self.cursor.fetchone()
        return True if record else False
    
    # Function used to close database cursor and connection objects.
    def close(self):
        try:
            self.cursor.close()
        except Exception:
            pass

        try:
            self.conn.close()
        except Exception:
            pass