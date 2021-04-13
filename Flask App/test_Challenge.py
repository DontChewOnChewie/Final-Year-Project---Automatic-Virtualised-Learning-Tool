import unittest
from Challenge import Challenge

class TestChallenge(unittest.TestCase):

    def test_succesful_difficulty_parse(self):
        challenge = Challenge(1, 1, "Test Name", "Test Description", 1, None, 123456789, "No Path")
        self.assertEqual(challenge.difficulty, challenge.DIFFICULTY_LEVELS[1])
    
    def test_unsuccesful_difficulty_parse(self):
        badIntValueChallenge = Challenge(1, 1, "Test Name", "Test Description", 5, None, 123456789, "No Path")
        self.assertEqual(badIntValueChallenge.difficulty, "Unknown")

        boolValueChallenge = Challenge(1, 1, "Test Name", "Test Description", True, None, 123456789, "No Path")
        self.assertEqual(boolValueChallenge.difficulty, "Unknown")

        noneValueChallenge = Challenge(1, 1, "Test Name", "Test Description", None, None, 123456789, "No Path")
        self.assertEqual(noneValueChallenge.difficulty, "Unknown")
        
        strValueChallenge = Challenge(1, 1, "Test Name", "Test Description", None, None, 123456789, "No Path")
        self.assertEqual(strValueChallenge.difficulty, "Unknown")