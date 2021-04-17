import unittest
import sqlite3
from SessionDao import SessionDao
from User import User

class TestSessionDao(unittest.TestCase):

    def test_check_session_exists(self):
        sdao = SessionDao(db_name="mocked_db.db")

        # Good session
        session = sdao.check_session_exists(1, "127.0.0.1")
        self.assertTrue(session)

        # Bad user id
        session = sdao.check_session_exists(2, "127.0.0.1")
        self.assertFalse(session)

        # Bad ip
        session = sdao.check_session_exists(1, "127.0.0.2")
        self.assertFalse(session)

        # Bad user id and ip
        session = sdao.check_session_exists(True, "127.0.0.2")
        self.assertFalse(session)

        sdao.close()
    
    def test_update_session_key(self):
        # Adding of session key
        user = User(3, "Not", "Needed", "Data", 12345678, 12345678, 0, 0)
        sdao = SessionDao(db_name="mocked_db.db")
        sdao.update_session_key(user, "127.0.0.1")
        sdao.conn.commit()

        connection = sqlite3.connect("mocked_db.db")
        cursor = connection.cursor()
        cursor.execute("SELECT ID FROM User_Session \
                        WHERE USER_ID = ?", (user.id,))
        result = cursor.fetchall()
        self.assertEqual(1, len(result))

        # Updating of session key
        cursor.execute("SELECT SESSION_KEY FROM User_Session \
                        WHERE USER_ID = ?", (user.id,))
        prev_key = cursor.fetchone()[0]
        sdao.update_session_key(user, "127.0.0.1")
        sdao.conn.commit()
        cursor.execute("SELECT SESSION_KEY FROM User_Session \
                        WHERE USER_ID = ?", (user.id,))
        new_key = cursor.fetchone()[0]
        self.assertNotEqual(prev_key, new_key)

        # Tidy up
        cursor.execute("DELETE FROM User_Session \
                        WHERE USER_ID = ?", (3,))
        cursor.close()
        connection.close()
        sdao.close()

    def test_create_session_key(self):
        sdao = SessionDao(db_name="mocked_db.db")
        key1 = sdao.create_session_key()
        key2 = sdao.create_session_key()
        self.assertNotEqual(key1, key2)
        sdao.close()
    
    def test_enable_auto_login(self):
        good_request = self._test_enable_auto_login_helper(1, "127.0.0.1")
        self.assertEqual(good_request, 1)

        bad_user_id_request = self._test_enable_auto_login_helper(2, "127.0.0.1")
        self.assertIsNone(bad_user_id_request)

        bad_ip_request = self._test_enable_auto_login_helper(1, "127.0.0.2")
        self.assertIsNone(bad_ip_request)
    
    def _test_enable_auto_login_helper(self, user_id, ip):
        sdao = SessionDao(db_name="mocked_db.db")
        sdao.enable_auto_login(user_id, ip)
        sdao.conn.commit()
        sdao.close()

        connection = sqlite3.connect("mocked_db.db")
        cursor = connection.cursor()
        cursor.execute("SELECT AUTOLOGIN FROM User_Session \
                        WHERE USER_ID = ? AND IP = ?", (user_id, ip))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result[0] if result else None
    
    def test_store_autologin_details(self):
        pass
    
    def test_get_auto_login_key(self):
        pass