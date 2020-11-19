import sqlite3
from User import User
from Challenge import Challenege

class ChallengeDAO:

    def __init__(self, conn=None):
        if not conn:
            self.conn = sqlite3.connect("db.db")
            self.cursor = self.conn.cursor()
        else:
            self.conn = conn
            self.cursor = self.conn.cursor()
    
    def check_challenge_for_user_exists(self, user_id, name):
        self.cursor.execute("SELECT ID FROM Challenge \
                             WHERE USER_ID = ? AND NAME = ?", (user_id, name))
        record = self.cursor.fetchone()
        return True if record else False

    def add_challenge(self, user_id, name, desc, difficulty):
        if not self.check_challenge_for_user_exists(user_id, name):
            self.cursor.execute("INSERT INTO Challenge (USER_ID, NAME, DESCRIPTION, DIFFICULTY) \
                                VALUES (?, ?, ?, ?)", (user_id, name, desc, difficulty))
            self.conn.commit()
            return Challenege(None, user_id, name, desc, difficulty, None)
        else:
            return "You already have a challenege with the same name uploaded."
    
    def get_challenge_by_id(self, id):
        self.cursor.execute("SELECT * FROM Challenge \
                            WHERE ID = ?", (id, ))
        record = self.cursor.fetchone()
        return Challenege(*record) if record else None

    def get_challenge_from_user_and_name(self, user_id, name):
        self.cursor.execute("SELECT ID FROM Challenge \
                            WHERE USER_ID = ? AND NAME = ?", (user_id, name))
        record = self.cursor.fetchone()
        return record[0] if record else None
    
    def get_author_of_challenge(self, challenge_id):
        self.cursor.execute("SELECT a.USERNAME FROM Challenge c \
                             JOIN Account a ON a.ID = c.USER_ID \
                             WHERE c.ID = ?", (challenge_id, ))
        record = self.cursor.fetchone()
        return record[0] if record else None
    
    def close(self):
        try:
            self.cursor.close()
        except Exception:
            pass

        try:
            self.conn.close()
        except Exception:
            pass