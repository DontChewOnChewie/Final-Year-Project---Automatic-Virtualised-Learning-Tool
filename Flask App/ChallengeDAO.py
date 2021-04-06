import sqlite3
from User import User
from Challenge import Challenge
from datetime import datetime

class ChallengeDAO:

    def __init__(self, conn=None):
        if not conn:
            self.conn = sqlite3.connect("db.db")
            self.cursor = self.conn.cursor()
        else:
            self.conn = conn
            self.cursor = self.conn.cursor()
    
    def add_banner_path_to_challenge_item(self, challenge_id, banner_path):
        self.cursor.execute("UPDATE Challenge \
                            SET BANNER_PATH = ? \
                            WHERE ID = ?", (banner_path, challenge_id))
        self.conn.commit()
    
    def check_challenge_for_user_exists(self, user_id, name):
        self.cursor.execute("SELECT ID FROM Challenge \
                             WHERE USER_ID = ? AND NAME = ?", (user_id, name))
        record = self.cursor.fetchone()
        return True if record else False

    def add_challenge(self, user_id, name, desc, difficulty):
        if not self.check_challenge_for_user_exists(user_id, name):
            timestamp = datetime.timestamp(datetime.now())
            self.cursor.execute("INSERT INTO Challenge (USER_ID, NAME, DESCRIPTION, DIFFICULTY, UPLOAD_DATE) \
                                VALUES (?, ?, ?, ?, ?)", (user_id, name, desc, difficulty, timestamp))
            self.conn.commit()
            return Challenge(None, user_id, name, desc, difficulty, None, timestamp, None)
        else:
            return "You already have a challenege with the same name uploaded."
    
    def get_challenge_by_id(self, id):
        self.cursor.execute("SELECT * FROM Challenge \
                            WHERE ID = ?", (id, ))
        record = self.cursor.fetchone()
        return Challenge(*record) if record else None

    def get_challenge_id_from_user_and_name(self, user_id, name):
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

    def get_recent_challenges(self):
        challenges = [x-x for x in range(7)]
        self.cursor.execute("SELECT * FROM Challenge \
                             ORDER BY UPLOAD_DATE DESC \
                             LIMIT 7")
        records = self.cursor.fetchall()
        for x in range(len(records)):
            challenges[x] = Challenge(*records[x])
        return challenges
    
    def get_users_uploaded_challenges(self, user_id):
        challenges = [x-x for x in range(7)]
        self.cursor.execute("SELECT c.* FROM Challenge c \
                             JOIN Account a ON a.ID = c.USER_ID \
                             WHERE a.ID = ? \
                             ORDER BY c.UPLOAD_DATE DESC \
                             LIMIT 7", (user_id, ))
        records = self.cursor.fetchall()
        for x in range(len(records)):
            challenges[x] = Challenge(*records[x])
        return challenges if len(records) > 0 else []
    
    def check_user_owns_challenge(self, user_id, challenge_id):
        self.cursor.execute("SELECT c.ID FROM Challenge c \
                             JOIN Account a on a.ID = c.USER_ID \
                             WHERE c.ID = ? AND c.USER_ID = ?", (challenge_id, user_id))
        record = self.cursor.fetchall()
        return True if len(record) > 0 else False
    
    def delete_challenge(self, challenge_id):
        self.cursor.execute("DELETE FROM Challenge \
                             WHERE ID = ?", (challenge_id,))
        self.conn.commit()
    
    def close(self):
        try:
            self.cursor.close()
        except Exception:
            pass

        try:
            self.conn.close()
        except Exception:
            pass