class Challenege:

    class Difficulty:
        BEGGINER = "begginer"
        INTERMEDIATE = "intermediate"
        ADVANCED = "advanced"

    class Technology:
        DOCKER = 1
        VB = 2

    def __init__(self, name, description, difficulty, image_path, technoligies):
        self.name = name
        self.description = description
        self.difficulty = difficulty
        self.image_path = image_path
        self.technoligies = technoligies