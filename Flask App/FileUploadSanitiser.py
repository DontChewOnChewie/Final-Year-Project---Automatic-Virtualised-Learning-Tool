from werkzeug.utils import secure_filename
import os

class FileUploadSanitiser:

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
            return False

        if not os.path.isdir(f"Challenges/{challenge_id}"):
            os.mkdir(f"Challenges/{challenge_id}")
        
        file.save(f"Challenges/{challenge_id}/banner{file_extesion}")
        return True

