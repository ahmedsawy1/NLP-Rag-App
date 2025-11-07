from fastapi import APIRouter, Depends, FastAPI, UploadFile, File
from helpers.config import get_settings

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile = File(...), 
                      app_settings: Settings = Depends(get_settings)):


    #   validate the file props