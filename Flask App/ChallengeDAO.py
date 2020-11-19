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
    

    def add_challenge(self, user_id, name, desc, difficulty):
        self.cursor.execute("INSERT INTO Challenge (USER_ID, NAME, DESCRIPTION, DIFFICULTY) \
                             VALUES (?, ?, ?, ?)", (user_id, name, desc, difficulty))
        self.conn.commit()
        return Challenege(user_id, name, desc, difficulty, None)
    
    def get_challenge_by_id(self, id):
        self.cursor.execute("SELECT * FROM Challenge \
                            WHERE ID = ?", (id, ))
        record = self.cursor.fetchone()
        return Challenege(*record[1:]) if record else None

    def get_challenge_from_user_and_name(self, user_id, name):
        self.cursor.execute("SELECT ID FROM Challenge \
                            WHERE USER_ID = ? AND NAME = ?", (user_id, name))
        record = self.cursor.fetchone()
        return record[0] if record else None
    
    def close():
        try:
            self.cursor.close()
        except Exception:
            pass

        try:
            self.conn.close()
        except Exception:
            pass