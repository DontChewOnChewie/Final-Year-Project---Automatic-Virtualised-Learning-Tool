import unittest
import sqlite3
from ChallengeDAO import ChallengeDAO
from Challenge import Challenge

class TestChallengeDAO(unittest.TestCase):

    def test_add_banner_path_to_challenge_item(self):
        good_challenge_id = self._test_add_banner_path_to_challenge_item_helper(1, "Path/To/Banner")
        self.assertIsNotNone(good_challenge_id)
        bad_challenge_id = self._test_add_banner_path_to_challenge_item_helper(10, "Path/To/Banner")
        self.assertIsNone(bad_challenge_id)
    
    def _test_add_banner_path_to_challenge_item_helper(self, challenge_id, banner_path):
        cdao = ChallengeDAO(db_name="mocked_db.db")
        cdao.add_banner_path_to_challenge_item(challenge_id, banner_path)
        cdao.close()

        connection = sqlite3.connect("mocked_db.db")
        cursor = connection.cursor()
        cursor.execute("SELECT BANNER_PATH FROM Challenge \
                        WHERE ID = ?", (challenge_id, ))
        record = cursor.fetchone()
        return record[0] if record else None
    
    def test_check_challenge_for_user_exists(self):
        cdao = ChallengeDAO(db_name="mocked_db.db")

        # Test good creds
        good_request = cdao.check_challenge_for_user_exists(1, "Test Challenge 1")
        self.assertTrue(good_request)

        # Test bad user id
        bad_user_id = cdao.check_challenge_for_user_exists(2, "Test Challenge 1")
        self.assertFalse(bad_user_id)

        # Test bad challenge name
        bad_challenge_name = cdao.check_challenge_for_user_exists(1, "Test Challenge 10")
        self.assertFalse(bad_challenge_name)

        # Test bad challenge name and user id
        bad_all_round = cdao.check_challenge_for_user_exists(2, "Test Challenge 10")
        self.assertFalse(bad_all_round)

        cdao.close()
    
    def test_add_challenge(self):
        pass

    def test_get_challenge_by_id(self):
        cdao = ChallengeDAO(db_name="mocked_db.db")

        # Test good challenge id
        good_id = cdao.get_challenge_by_id(1)
        self.assertIsInstance(good_id, Challenge)

        # Test bad challenge id
        bad_id = cdao.get_challenge_by_id(10)
        self.assertIsNone(bad_id)

        cdao.close()
    
    def test_get_challenge_id_from_user_and_name(self):
        cdao = ChallengeDAO(db_name="mocked_db.db")

        # Test good request
        good_request = cdao.get_challenge_id_from_user_and_name(1, "Test Challenge 1")
        self.assertEqual(good_request, 1)

        # Test bad user id
        bad_id = cdao.get_challenge_id_from_user_and_name(2, "Test Challenge 1")
        self.assertIsNone(bad_id)

        # Test bad challenge name
        bad_challenge_name = cdao.get_challenge_id_from_user_and_name(1, "Test Challenge 2")
        self.assertIsNone(bad_challenge_name)

        # Test bad challenge name and user id
        bad_all_round = cdao.get_challenge_id_from_user_and_name(10, "Test Challenge 10")
        self.assertIsNone(bad_all_round)

        cdao.close()
    
    def test_get_author_of_challenge(self):
        cdao = ChallengeDAO(db_name="mocked_db.db")

        # Test good challenge id
        good_id = cdao.get_author_of_challenge(1)
        self.assertEqual(good_id, "Test User 1")

        # Test bad challenge id
        bad_id = cdao.get_author_of_challenge(10)
        self.assertIsNone(bad_id)

        cdao.close()
    
    def test_get_recent_challenges(self):
        cdao = ChallengeDAO(db_name="mocked_db.db")
        challenges = cdao.get_recent_challenges()
        self.assertEqual(len(challenges), 7)
        cdao.close()

    def test_get_users_uploaded_challenges(self):
        cdao = ChallengeDAO(db_name="mocked_db.db")

        # Test user with challenges
        challenges = cdao.get_users_uploaded_challenges(1)
        self.assertEqual(len(challenges), 7)

        # Test user with no challenges
        no_challenges = cdao.get_users_uploaded_challenges(3)
        self.assertEqual(no_challenges, [])

        # Test bad user id
        bad_user_id = cdao.get_users_uploaded_challenges(10)
        self.assertEqual(bad_user_id, [])

        cdao.close()

    def test_check_user_owns_challenge(self):
        cdao = ChallengeDAO(db_name="mocked_db.db")

        # Test user owns challenge
        user_owns = cdao.check_user_owns_challenge(1, 1)
        self.assertTrue(user_owns)

        # Test user does not own challenge
        user_not_owns = cdao.check_user_owns_challenge(1, 2)
        self.assertFalse(user_not_owns)

        cdao.close()

    def test_delete_challenge(self):
        connection = sqlite3.connect("mocked_db.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Challenge (USER_ID, NAME, DESCRIPTION, DIFFICULTY, UPLOAD_DATE) \
                        VALUES (?, ?, ?, ?, ?)", (1, "Challenge to Delete", "To be deleted.", 1, 123456789))
        connection.commit()
        cursor.close()
        connection.close()

        cdao = ChallengeDAO(db_name="mocked_db.db")
        cdao.delete_challenge(3)
        cdao.close()

        connection = sqlite3.connect("mocked_db.db")
        cursor = connection.cursor()
        cursor.execute("SELECT ID FROM Challenge \
                        WHERE ID = ?", (3, ))
        record = cursor.fetchone()
        cursor.close()
        connection.close()
        self.assertIsNone(record)

            