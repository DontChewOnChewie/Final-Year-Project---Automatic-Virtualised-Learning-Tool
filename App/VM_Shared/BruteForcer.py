from zipfile import ZipFile
from string import ascii_letters, punctuation
import threading
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

class BruteForcer:

    def __init__(self, target, pass_length):
        self.target = target
        self.pass_length = pass_length
        self.list = ascii_letters + punctuation + "".join(numbers)
        self.cracked = False

    def start(self):
        self.crack("")

    def crack(self, word):
        for letter in self.list:
            attempt = word + letter
            if len(attempt) <= self.pass_length and not self.cracked:
                self.attempt_password(attempt)    
                t = threading.Thread(name=attempt, target=self.crack(attempt))
                t.start()

    def attempt_password(self, password):
        with ZipFile(self.target) as file:
            try:
                if not self.cracked:
                    print(f"Attempting password {password}.")
                    file.extractall(pwd=bytes(password, 'utf-8'))
                    print(f"Successfully cracked, the password is {password}.")
                    self.cracked = True
                    exit()
            except:
                pass

if __name__ == "__main__":
    bf = BruteForcer("Target.zip", 5)
    bf.start()