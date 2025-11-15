from fastapi import FastAPI
# from routes.base import base_router
# from routes.data import data_router
from routes import base, data
from helpers.config import get_settings

app = FastAPI()

# After each event, make an action
@app.on_event("startup")
async def startup_db_client():
    app_settings = get_settings()
    print("----- app settings -----")
    print(app_settings)

app.include_router(base.base_router)
app.include_router(data.data_router)
