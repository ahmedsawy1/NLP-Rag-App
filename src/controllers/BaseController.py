from helpers.config import get_settings
import os 

class BaseController:
    
    def __init__(self):
        self.app_settings = get_settings()
        # To get the current file directory => src/
        self.build_dir = os.path.dirname(os.path.abspath(__file__))

        # To get the files directory => src/assets/files
        self.files_dir = os.path.join(self.build_dir, "assets/files")
        # Make the same thing but top is better because it will be good for all operating systems
        # self.files_dir = self.build_dir + "/assets/files"