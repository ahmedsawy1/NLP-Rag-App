from .BaseController import BaseController
from .ProjectController import ProjectController
from enums import ResponseMessageEnums
from fastapi import UploadFile
import re
import os

# DataController extends BaseController to provide data-specific operations.
class DataController(BaseController):
    def __init__(self):
        super().__init__()  # Initialize BaseController to set up shared resources and state.

    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_EXTENSIONS:
            return {
                "success": False,
                "error": ResponseMessageEnums.FILE_TYPE_NOT_ALLOWED.value
            }

        if file.size > self.app_settings.FILE_MAX_SIZE:
            return {
                "success": False,
                "error": ResponseMessageEnums.FILE_SIZE_TOO_LARGE.value
            }

        return {
            "success": True,
            "message": ResponseMessageEnums.FILE_UPLOADED_SUCCESSFULLY.value
        }

    def generate_unique_file_path(self, origin_file_name: str, project_id: str):
        random_file_key = self.generate_random_string()
        project_dir_path = ProjectController().get_project_path(project_id=project_id)
        clean_file_name = self.get_clean_file_name(origin_file_name=origin_file_name)

        file_extension = os.path.splitext(origin_file_name)[1]
        file_name_str = f"{clean_file_name}_{random_file_key}{file_extension}"

        new_file_path=os.path.join(project_dir_path, file_name_str)
        
        while os.path.exists(new_file_path):
            random_file_key = self.generate_random_string()
            new_file_path=os.path.join(project_dir_path, file_name_str)
        
        return new_file_path, file_name_str

    def get_clean_file_name(self, origin_file_name: str):
        # Remove special characters from the file name
        cleaned_file_name = re.sub(r'[^\w.]', '', origin_file_name.strip())
        # Replace spaces with underscores
        cleaned_file_name = cleaned_file_name.replace(" ", "_")
        
        return cleaned_file_name