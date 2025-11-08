from helpers.config import get_settings
import os 

class BaseController:
    
    def __init__(self):
        self.app_settings = get_settings()
        # To get the current file directory => src/controllers
        self.build_dir = os.path.dirname(os.path.abspath(__file__))

        # To get the project root directory => src/
        self.project_root_dir = os.path.dirname(self.build_dir)

        # To get the files directory => src/assets/files
        self.files_dir = os.path.join(self.project_root_dir, "assets", "files")
        # Make the same thing but top is better because it will be good for all operating systems
        # self.files_dir = self.build_dir + "/assets/files"

        if not os.path.exists(self.files_dir):
            os.makedirs(self.files_dir, exist_ok=True)