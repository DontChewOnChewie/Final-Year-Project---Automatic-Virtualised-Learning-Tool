import os

class UploadHandler:

    CHALLENGE_BANNER_DIR = "static/images/Challenges/"

    def __init__(self):
        pass
    
    def save_challenege_banner(self, challenge_id, file):
        allowed_extensions = [".png", "jpeg", ".jpg", ".jfif", ".svg"]
        file_extesion = None
        for ext in allowed_extensions:
            if file.filename.endswith(ext):
                file_extesion = ext
                break
        
        if not file_extesion:
            return "File could not be uploaded, file type must be png, jpg, jpeg or svg."
        
        file.save(f"{self.CHALLENGE_BANNER_DIR}{challenge_id}{file_extesion}")
        return True
    
    def get_upload_banner_path(self, challenge_id):
        files = os.listdir(f"{self.CHALLENGE_BANNER_DIR}")
        print(challenge_id)
        for file in files:
            print(file.split("."))
            if file.split(".")[0] == challenge_id:
                return "/" + self.CHALLENGE_BANNER_DIR + file
        return None

