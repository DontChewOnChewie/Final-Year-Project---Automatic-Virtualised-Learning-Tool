import sqlite3
import random
from string import ascii_letters
from datetime import datetime
from User import User

'''
Class used to manage data access to the User_Session table in the database.
Autologin functions are not fully implemented into the program yet and will be
a future development.
'''
class SessionDao:

    SESSION_KEY_LENGTH = 50

    # Constructor for SessionDao object.
    # cursor = Active database cursor.
    # db_name = Name of database file to connect to.
    def __init__(self, cursor=None, db_name="db.db"):
        if not cursor:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
        else:
            self.cursor = cursor

    # Function used to check if a users session exists.
    def check_session_exists(self, user_id, ip):
        if isinstance(user_id, bool):
            return False

        self.cursor.execute("SELECT * FROM User_Session \
                             WHERE USER_ID = ? AND IP = ?", (user_id, ip))
        record = self.cursor.fetchone()
        return True if record else False

    # Function used to update a users session key.
    def update_session_key(self, user, ip):
        timestamp = datetime.timestamp(datetime.now())
        key = self.create_session_key()
        if self.check_session_exists(user.id, ip):
            self.cursor.execute("UPDATE User_Session \
                                SET SESSION_KEY = ?, CREATION_DATE = ? \
                                WHERE IP = ? AND USER_ID = ?", (key, timestamp, ip, user.id))
        else:
            self.cursor.execute("INSERT INTO User_Session (SESSION_KEY, USER_ID, IP, CREATION_DATE)\
                                 VALUES (?, ?, ?, ?)", (key, user.id, ip, timestamp))
        return key

    # Function used to create a brand new random session key.
    def create_session_key(self):
        rand = random.Random()
        key = ""
        for i in range(self.SESSION_KEY_LENGTH):
            key = key + ascii_letters[rand.randint(0, len(ascii_letters) -1)]
        return key
    
    # Function used to enable auto login field.
    def enable_auto_login(self, user_id, ip):
        self.cursor.execute("UPDATE User_Session \
                             SET AUTOLOGIN = 1 \
                             WHERE USER_ID = ? AND IP = ?", (user_id, ip))
    
    # Function used to store a user given autlogin details.
    def store_autologin_details(self, user_id, ip, secret_key, iv, key):
        self.cursor.execute("UPDATE User_Session \
                             SET ENCRYPTED_AUTOLOGIN_KEY = ?, ENCRYPT_KEY = ?, IV_KEY = ? \
                             WHERE USER_ID = ? AND IP = ?", (key, secret_key, iv, user_id, ip))
        self.conn.commit()
    
    # Function used to get a users autologin key.
    def get_auto_login_key(self, data, ip):
        self.cursor.execute(f"SELECT * FROM User_Session \
                             WHERE ENCRYPTED_AUTOLOGIN_KEY LIKE '{data}%'")
        record = self.cursor.fetchone()
        if not record:
            return "Something went wrong with your auto login credentials."

        return record if record[3] == ip else "Something went wrong with your auto login credentials."
    
    # Function used to close both cursor and connection objects.
    def close(self):
        try:
            self.cursor.close()
        except Exception:
            pass

        try:
            self.conn.close()
        except Exception:
            pass