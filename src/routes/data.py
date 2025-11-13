from fastapi import APIRouter, Depends, UploadFile, File, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController
import aiofiles
import os
import logging
from routes.schemas import PossessRequest

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile = File(...), 
                      app_settings: Settings = Depends(get_settings)):


    validation_result = DataController().validate_uploaded_file(file)

    if not validation_result.get("success"):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "error": validation_result.get("error")
            },
        )

    project_dir_path = ProjectController().get_project_path(project_id=project_id)

    file_path, file_id = DataController().generate_unique_file_path(origin_file_name=file.filename, project_id=project_id)
    # file_path = os.path.join(project_dir_path, file.filename)

    try:
        # wb => write binary
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)

    except Exception as e:
        print(e)
        logger.error(f"Failed to upload file: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": response_message_enums.FILE_UPLOAD_FAILED.value
            },
        )

    print("validation_result")         
    print(validation_result)         

    return {**validation_result, **{"file id": file_id}}


@data_router.post("/process/{project_id}")
async def possess_endpoint(project_id: str, process_request: PossessRequest):
    file_id = process_request.file_id
    
    return file_id