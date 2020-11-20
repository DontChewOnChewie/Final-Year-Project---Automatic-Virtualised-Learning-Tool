import os
import zipfile
import shutil

class UploadHandler:

    CHALLENGE_BANNER_DIR = "static/Challenges/"

    ALLOWED_EXTENSIONS = { "Docker":["zip"], "VirtualBox":["vdi", "vmdk"]}

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
        
        if not os.path.isdir(f"{self.CHALLENGE_BANNER_DIR}{challenge_id}"):
            os.mkdir(f"{self.CHALLENGE_BANNER_DIR}{challenge_id}")
        
        file.save(f"{self.CHALLENGE_BANNER_DIR}{challenge_id}/banner{file_extesion}")
        return True
    
    def get_upload_banner_path(self, challenge_id):
        files = os.listdir(f"{self.CHALLENGE_BANNER_DIR}{challenge_id}/")
        for file in files:
            if file.split(".")[0] == "banner":
                return f"/{self.CHALLENGE_BANNER_DIR}{challenge_id}/{file}" 
        return None

    def check_challenge_extensions(self, values):
        for key in values.keys():
            if values[key][0] != "Other":
                ext = values[key][1].filename.split(".")[-1]
                if ext not in self.ALLOWED_EXTENSIONS[values[key][0]]:
                    print(f"Extension {ext} not allowed for {values[key][0]}")
                    return False
        return True

    def save_challenge_files(self, values, challenge_id):
        if not os.path.isdir(f"{self.CHALLENGE_BANNER_DIR}{challenge_id}/"):
            os.mkdir(f"{self.CHALLENGE_BANNER_DIR}{challenge_id}")
        
        if not os.path.isdir(f"{self.CHALLENGE_BANNER_DIR}{challenge_id}/build/"):
            os.mkdir(f"{self.CHALLENGE_BANNER_DIR}{challenge_id}/build/")
        
        if self.check_challenge_extensions(values):
            saved_files = []
            for key in values.keys():
                filename = key + "." + values[key][1].filename.split(".")[-1]
                print(f"Saving file {filename}.")
                values[key][1].save(f"{self.CHALLENGE_BANNER_DIR}{challenge_id}/build/{filename}")
                saved_files.append(filename)
                print(f"File {filename} saved.")
            
            zipf = zipfile.ZipFile(f"{self.CHALLENGE_BANNER_DIR}{challenge_id}/build.zip", 'w', zipfile.ZIP_DEFLATED)
            for file in saved_files:
                zipf.write(f"{self.CHALLENGE_BANNER_DIR}{challenge_id}/build/{file}")
            zipf.close()

            shutil.rmtree(f"{self.CHALLENGE_BANNER_DIR}{challenge_id}/build", ignore_errors=True)
            return True
        
        shutil.rmtree(f"{self.CHALLENGE_BANNER_DIR}{challenge_id}/build", ignore_errors=True)
        return False

        

        

