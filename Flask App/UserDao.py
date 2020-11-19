import hashlib
import sqlite3
from datetime import datetime
from User import User
from string import ascii_letters
import random
from SessionDao import SessionDao

class UserDao:

    def __init__(self, cursor=None):
        if not cursor:
            self.conn = sqlite3.connect("db.db")
            self.cursor = self.conn.cursor()
        else:
            self.cursor = cursor

    def hash_password(self, password):
        return hashlib.sha512(password.encode('utf-8')).hexdigest()

    def check_account_exists(self, credentials):
        self.cursor.execute("SELECT USERNAME, EMAIL\
                             FROM Account \
                             WHERE USERNAME = ? AND EMAIL = ?", (credentials[0], credentials[1]))
        record = self.cursor.fetchone()
        return True if record else False
    
    def get_user_id_from_name_and_email(self, username, email):
        self.cursor.execute("SELECT ID FROM Account\
                             WHERE USERNAME = ? AND EMAIL = ?", (username, email))
        record = self.cursor.fetchone()
        return record[0]
    
    def get_user_id_from_name_and_session_key(self, username, session_key):
        self.cursor.execute("SELECT a.ID FROM Account a \
                             JOIN User_Session u ON a.ID = u.USER_ID \
                             WHERE a.USERNAME = ? AND u.SESSION_KEY = ?", (username, session_key))
        record = self.cursor.fetchone()
        return record[0]
    
    def get_user_from_username(self, username):
        self.cursor.execute("SELECT * FROM Account \
                             WHERE USERNAME = ?", (username,))
        record = self.cursor.fetchone()
        return User(*record) if record else None


    def signup(self, credentials, ip, auto_login):
        try:
            timestamp = datetime.timestamp(datetime.now())
            self.cursor.execute("INSERT INTO Account (USERNAME, EMAIL, PASSWORD, SIGN_UP_DATE, LAST_SIGN_IN)\
                                VALUES (?, ?, ?, ?, ?)", (credentials[0].lower(), 
                                                        credentials[1],
                                                        self.hash_password(credentials[2]),
                                                        timestamp,
                                                        timestamp))
            id = self.get_user_id_from_name_and_email(credentials[0], credentials[1])
            user = User(id, credentials[0], credentials[1], credentials[2], timestamp, timestamp, 0, 0)
            sdao = SessionDao(self.cursor)
            key = sdao.update_session_key(user, ip)

            if auto_login:
                sdao.enable_auto_login(user.id, ip)
            self.conn.commit()
            sdao.close()
        except sqlite3.IntegrityError:
            return f"Username {credentials[0]} is already taken, please try again."

        return [user, key]

    def login(self, credentials, ip, auto_login):
        self.cursor.execute("SELECT * FROM Account \
                            WHERE USERNAME = ? AND EMAIL = ? AND PASSWORD = ?", (credentials[0],
                                                                                 credentials[1],
                                                                                 self.hash_password(credentials[2])))
        record = self.cursor.fetchone()

        if record:
            user = User(*record)
            sdao = SessionDao(self.cursor)
            key = sdao.update_session_key(user, ip)
            if auto_login:
                sdao.enable_auto_login(user.id, ip)
            self.conn.commit()
            sdao.close()

        return [user, key] if record else "Password for account credentials inccorect"

    def auto_login(self, username, key):
        self.cursor.execute("SELECT a.* FROM Account a \
                             JOIN User_Session u ON a.ID = u.USER_ID \
                             WHERE a.USERNAME = ? AND u.SESSION_KEY = ?", (username, key))
        record = self.cursor.fetchone()
        return User(*record)

    def check_session_key(self, user, session_key):
        self.cursor.execute("SELECT a.ID FROM Account a \
                             JOIN User_Session u ON a.ID = u.USER_ID \
                             WHERE a.USERNAME = ? AND u.SESSION_KEY = ?", (user, session_key))
        record = self.cursor.fetchone()
        return True if record else False
    
    def close(self):
        try:
            self.cursor.close()
        except Exception:
            pass

        try:
            self.conn.close()
        except Exception:
            pass