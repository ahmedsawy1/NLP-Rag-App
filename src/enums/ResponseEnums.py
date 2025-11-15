from enum import Enum

class ResponseMessageEnums(Enum):
    FILE_UPLOADED_SUCCESSFULLY = "File uploaded successfully"
    FILE_UPLOAD_FAILED = "File uploaded failed"
    FILE_UPLOAD_IN_PROGRESS = "File uploaded in progress"
    FILE_UPLOAD_COMPLETED = "File uploaded completed"
    FILE_TYPE_NOT_ALLOWED = "File type not allowed"
    FILE_SIZE_TOO_LARGE = "File size too large"
    PROCESS_FILE_CONTENT_FAILED = "Process file content failed"
    PROCESS_FILE_CONTENT_SUCCESS = "Process file content successfully"