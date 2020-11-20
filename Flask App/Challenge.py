class Challenge:

    class Technology:
        DOCKER = 1
        VB = 2

    DIFFICULTY_LEVELS = { 1:"Begginer", 2:"Intermediate", 3:"Advanced" }

    def __init__(self, id, user_id, name, description, difficulty, technoligies, upload_timestamp):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.description = description
        self.difficulty = self.DIFFICULTY_LEVELS[difficulty]
        self.technoligies = technoligies
        self.upload_timestamp = upload_timestamp