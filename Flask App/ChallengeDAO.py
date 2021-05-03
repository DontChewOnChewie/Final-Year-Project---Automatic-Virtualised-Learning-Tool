import sqlite3
from User import User
from Challenge import Challenge
from datetime import datetime

'''
Class used to manage data access to the Challenge table
within db.db.
'''
class ChallengeDAO:

    # Constructor for ChallengeDAO object.
    # conn = database connection.
    # db_name = name of database to access.
    def __init__(self, conn=None, db_name="db.db"):
        if not conn:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
        else:
            self.conn = conn
            self.cursor = self.conn.cursor()
    
    # Function used to add a banners file path to a challege.
    def add_banner_path_to_challenge_item(self, challenge_id, banner_path):
        self.cursor.execute("UPDATE Challenge \
                            SET BANNER_PATH = ? \
                            WHERE ID = ?", (banner_path, challenge_id))
        self.conn.commit()
    
    # Function used to check if a user already has a challenge with same name.
    def check_challenge_for_user_exists(self, user_id, name):
        self.cursor.execute("SELECT ID FROM Challenge \
                             WHERE USER_ID = ? AND NAME = ?", (user_id, name))
        record = self.cursor.fetchone()
        return True if record else False

    # Function used to add a challenge to the database.
    # Return this new challenge object.
    def add_challenge(self, user_id, name, desc, difficulty):
        if not self.check_challenge_for_user_exists(user_id, name):
            timestamp = datetime.timestamp(datetime.now())
            self.cursor.execute("INSERT INTO Challenge (USER_ID, NAME, DESCRIPTION, DIFFICULTY, UPLOAD_DATE) \
                                VALUES (?, ?, ?, ?, ?)", (user_id, name, desc, difficulty, timestamp))
            self.conn.commit()
            return Challenge(None, user_id, name, desc, difficulty, None, timestamp, None)
        else:
            return "You already have a challenege with the same name uploaded."
    
    # Function used the get a challenges data by its ID.
    def get_challenge_by_id(self, id):
        self.cursor.execute("SELECT * FROM Challenge \
                            WHERE ID = ?", (id, ))
        record = self.cursor.fetchone()
        return Challenge(*record) if record else None

    # Function used to get a challenges ID from a given user ID and challenge name.
    def get_challenge_id_from_user_and_name(self, user_id, name):
        self.cursor.execute("SELECT ID FROM Challenge \
                            WHERE USER_ID = ? AND NAME = ?", (user_id, name))
        record = self.cursor.fetchone()
        return record[0] if record else None
    
    # Function used to get the author of a give challenge by that challenges ID.
    def get_author_of_challenge(self, challenge_id):
        self.cursor.execute("SELECT a.USERNAME FROM Challenge c \
                             JOIN Account a ON a.ID = c.USER_ID \
                             WHERE c.ID = ?", (challenge_id, ))
        record = self.cursor.fetchone()
        return record[0] if record else None

    # Function used to get the 7 most recent uploaded challenges.
    def get_recent_challenges(self):
        challenges = [x-x for x in range(7)]
        self.cursor.execute("SELECT * FROM Challenge \
                             ORDER BY UPLOAD_DATE DESC \
                             LIMIT 7")
        records = self.cursor.fetchall()
        for x in range(len(records)):
            challenges[x] = Challenge(*records[x])
        return challenges
    
    # Function used to get the latest 7 uploaded challenges of a particular user.
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
    
    # Function used to check if a user owns a challenge based on IDs.
    def check_user_owns_challenge(self, user_id, challenge_id):
        self.cursor.execute("SELECT c.ID FROM Challenge c \
                             JOIN Account a on a.ID = c.USER_ID \
                             WHERE c.ID = ? AND c.USER_ID = ?", (challenge_id, user_id))
        record = self.cursor.fetchall()
        return True if len(record) > 0 else False

   # Function used to remove a challenge from the database. 
    def delete_challenge(self, challenge_id):
        self.cursor.execute("DELETE FROM Challenge \
                             WHERE ID = ?", (challenge_id,))
        self.conn.commit()
    
    # Function used to close both database cursor and conncetions.
    def close(self):
        try:
            self.cursor.close()
        except Exception:
            pass

        try:
            self.conn.close()
        except Exception:
            pass