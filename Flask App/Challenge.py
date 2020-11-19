class Challenege:

    class Technology:
        DOCKER = 1
        VB = 2

    DIFFICULTY_LEVELS = { 1:"Begginer", 2:"Intermediate", 3:"Advanced" }

    def __init__(self, user_id, name, description, difficulty, technoligies):
        print(difficulty)
        self.user_id = user_id
        self.name = name
        self.description = description
        self.difficulty = self.DIFFICULTY_LEVELS[difficulty]
        self.technoligies = technoligies