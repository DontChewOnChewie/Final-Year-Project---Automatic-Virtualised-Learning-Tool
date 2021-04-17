import unittest
import sqlite3
from UserDao import UserDao
from User import User

class TestUserDao(unittest.TestCase):

    def test_hash_password(self):
        udao = UserDao(db_name="mocked_db.db")

        hashed_password = udao.hash_password("password")
        self.assertEqual(hashed_password, 'b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86')
        
        udao.close()
    
    def test_check_account_exists(self):
        udao = UserDao(db_name="mocked_db.db")

        # Test valid user
        user_exists = udao.check_account_exists(["Test User 1", "testuser1@test.com"])
        self.assertTrue(user_exists)

        # Test invalid user
        user_exists = udao.check_account_exists(["Test User 10", "testuser1@test.com"])

        self.assertFalse(user_exists)
        udao.close()
    
    def test_get_user_id_from_name_and_email(self):
        udao = UserDao(db_name="mocked_db.db")

        # Test valid user
        user_id = udao.get_user_id_from_name_and_email("Test User 1", "testuser1@test.com")
        self.assertTrue(isinstance(user_id, int))

        #Test invalid user
        user_id = udao.get_user_id_from_name_and_email("Test User 1", "testuser2@test.com")
        self.assertIsNone(user_id)
        
        udao.close()
    
    def test_get_user_id_from_name_and_session_key(self):
        udao = UserDao(db_name="mocked_db.db")

        # Test user with session key
        result = udao.get_user_id_from_name_and_session_key("Test User 1", "sIdIyofEKJXXFaAUNmUQpvkZJYPEDFIoBRvSoTLMjecZnajeCl")
        self.assertEqual(result, 1)

        # Test user without session key
        result = udao.get_user_id_from_name_and_session_key("Test User 2", "sIdIyofEKJXXFaAUNmUQpvkZJYPEDFIoBRvSoTLMjecZnajeCl")
        self.assertIsNone(result)

        udao.close()
    
    def test_get_user_from_username(self):
        udao = UserDao(db_name="mocked_db.db")

        # Test valid user
        user = udao.get_user_from_username("Test User 1")
        self.assertTrue(isinstance(user, User))

        #Test invalid user
        user = udao.get_user_from_username("Test User 10")
        self.assertIsNone(user)

        udao.close()
    
    def test_update_last_login(self):
        udao = UserDao(db_name="mocked_db.db")

        connection = sqlite3.connect("mocked_db.db")
        cursor = connection.cursor()
        cursor.execute("SELECT LAST_SIGN_IN from Account \
                        WHERE ID = ?", (1, ))
        prev_timestamp = cursor.fetchone()[0]

        udao.update_last_login(1)
        cursor.execute("SELECT LAST_SIGN_IN from Account \
                        WHERE ID = ?", (1, ))
        new_timestamp = cursor.fetchone()[0]
        self.assertNotEqual(prev_timestamp, new_timestamp)
    
    def test_signup(self):
        udao = UserDao(db_name="mocked_db.db")
        new_creds = ["Added User", "addeduser@gmail.com", "password"]

        # Test good signup
        result = udao.signup(new_creds, "127.0.0.1", None)
        self.assertIsInstance(result[0], User)
        self.assertEqual(len(result[1]), 50)

        connection = sqlite3.connect("mocked_db.db")
        cursor = connection.cursor()
        cursor.execute("SELECT ID FROM Account \
                        WHERE USERNAME = ?", ("Added User", ))
        result = cursor.fetchone()
        self.assertEqual(len(result), 1)
        udao.close()

        # Test for same username exception
        udao = UserDao(db_name="mocked_db.db")
        result = udao.signup(["Test User 1", "samename@gmail.com", "password"], "127.0.0.1", None)
        self.assertIsInstance(result, str)
        udao.close()

        # Tidy up
        cursor.execute("DELETE FROM User_Session \
                        WHERE USER_ID IN \
                        (SELECT ID FROM Account WHERE USERNAME = ?)", ("Added User", ))
        cursor.execute("DELETE FROM Account \
                        WHERE USERNAME = ?", ("Added User", ))
        connection.commit()
        cursor.close()
        connection.close()
    
    def test_login(self):
        udao = UserDao(db_name="mocked_db.db")

        # Test successful login
        result = udao.login(["Test User 1", "testuser1@test.com", "password"], "127.0.0.1", None)
        self.assertIsInstance(result[0], User)
        self.assertEqual(len(result[1]), 50)
        udao.close()

        # Test unsuccessful login
        udao = UserDao(db_name="mocked_db.db")
        result = udao.login(["Test User 1", "testuser1@gmail.com", "pasword"], "127.0.0.1", None)
        self.assertEqual(result, "Password for account credentials inccorect")
        udao.close()

        # Tidy up
        connection = sqlite3.connect("mocked_db.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE User_Session \
                        SET SESSION_KEY = ? \
                        WHERE USER_ID = ?", ("sIdIyofEKJXXFaAUNmUQpvkZJYPEDFIoBRvSoTLMjecZnajeCl", 1))

        connection.commit()
        cursor.close()
        connection.close()
    
    def test_auto_login(self):
        pass

    def test_check_session_key(self):
        udao = UserDao(db_name="mocked_db.db")
        # Good creds
        good_key = udao.check_session_key("Test User 1", "sIdIyofEKJXXFaAUNmUQpvkZJYPEDFIoBRvSoTLMjecZnajeCl")
        self.assertTrue(good_key)

        # Bad key cred
        bad_key = udao.check_session_key("Test User 1", "sIdIyofEKJXXFaAUNmUQpvkZJYPEDFIoBRvSoTLMjecZnajeC2")
        self.assertFalse(bad_key)

        # Bad user cred
        bad_user = udao.check_session_key("Test User 2", "sIdIyofEKJXXFaAUNmUQpvkZJYPEDFIoBRvSoTLMjecZnajeCl")
        self.assertFalse(bad_user)

        # Bad user and key cred
        bad_key_user = udao.check_session_key("Test User 2", "sIdIyofEKJXXFaAUNmUQpvkZJYPEDFIoBRvSoTLMjecZnajeC2")
        self.assertFalse(bad_key_user)

        udao.close()