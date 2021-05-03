'''
Class used as a model for Challenge items.
'''
class Challenge:

    class Technology:
        DOCKER = 1
        VB = 2

    DIFFICULTY_LEVELS = { 1:"Begginer", 2:"Intermediate", 3:"Advanced" }

    # Constructor for Challenge object.
    def __init__(self, id, user_id, name, description, difficulty, technoligies, upload_timestamp, banner_path):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.description = description
        self.difficulty = self.set_difficulty_level(difficulty)
        self.technoligies = technoligies
        self.upload_timestamp = upload_timestamp
        self.banner_path = banner_path
    
    # Function used to set difficulty to string from given integer.
    def set_difficulty_level(self, difficulty):
        if isinstance(difficulty, bool):
            return "Unknown"

        try:
            return self.DIFFICULTY_LEVELS[difficulty]
        except KeyError:
            return "Unknown"  