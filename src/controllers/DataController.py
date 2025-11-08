from .BaseController import BaseController
from fastapi import UploadFile

# DataController extends BaseController to provide data-specific operations.
class DataController(BaseController):
    def __init__(self):
        super().__init__()  # Initialize BaseController to set up shared resources and state.

    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_EXTENSIONS:
            return False

        if file.size > self.app_settings.FILE_MAX_SIZE:
            return False

        return True
