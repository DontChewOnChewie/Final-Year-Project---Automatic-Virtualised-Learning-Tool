import os
import zipfile
import shutil
from ChallengeDAO import ChallengeDAO

'''
Class used to manage any user upload or deletion from the server.
'''
class UploadHandler:

    CHALLENGE_BANNER_DIR = "static/Challenges/"

    ALLOWED_EXTENSIONS = { "Docker":["zip"], "VirtualBox":["vdi", "vmdk", "iso"]}

    # Constructor for UploadHandler object.
    def __init__(self):
        pass
    
    # Function used to save an uploaded banner image for a challenge.
    # Extension is first check before doing so.
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
        cdao = ChallengeDAO()
        cdao.add_banner_path_to_challenge_item(challenge_id, f"/{self.CHALLENGE_BANNER_DIR}{challenge_id}/banner{file_extesion}")
        cdao.close()
        return True
    
    # Function used to retrieve the path of a banner image for given challenge ID.
    def get_upload_banner_path(self, challenge_id):
        try:
            files = os.listdir(f"{self.CHALLENGE_BANNER_DIR}{challenge_id}/")
            for file in files:
                if file.split(".")[0] == "banner":
                    return f"/{self.CHALLENGE_BANNER_DIR}{challenge_id}/{file}"
        except:
            return None

    # Function used to check if uploaded lesson files are of the correct file type.
    def check_challenge_extensions(self, values):
        for key in values.keys():
            if values[key][0] != "Other":
                ext = values[key][1].filename.split(".")[-1]
                if ext not in self.ALLOWED_EXTENSIONS[values[key][0]]:
                    print(f"Extension {ext} not allowed for {values[key][0]}")
                    return False
        return True

    # Function used to save validated uploaded lesson files to the server.
    # These files are then compiled into a zip file for easy download by the user.
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
    
    # Function used to save a lesson file to an uploaded challenge.
    # This file is written in lesson.json and is zipped up with
    # the previously uploaded files.
    def save_lesson_file(self, json, challenge_id):
        if not os.path.isfile(f"{self.CHALLENGE_BANNER_DIR}{challenge_id}/build.zip"):
            return False
        
        with open(f"{self.CHALLENGE_BANNER_DIR}{challenge_id}/lesson.json", "w") as json_file:
            json_file.write(json)
                
        zipf = zipfile.ZipFile(f"{self.CHALLENGE_BANNER_DIR}{challenge_id}/build.zip", "a")
        zipf.write(f"{self.CHALLENGE_BANNER_DIR}{challenge_id}/lesson.json")
        zipf.close()

        os.remove(f"{self.CHALLENGE_BANNER_DIR}{challenge_id}/lesson.json")
        return True
    
    # Function used to remove a challenges files from the server.
    def remove_challenge(self, challenge_id):
        if os.path.isdir(f"{self.CHALLENGE_BANNER_DIR}{challenge_id}"):
            shutil.rmtree(f"{self.CHALLENGE_BANNER_DIR}{challenge_id}", ignore_errors=True)
        

        

        

