from fastapi import FastAPI
from routes import base
from helpers import get_settings
from motor.motor_asyncio import AsyncIOMotorClient


app = FastAPI()

# After each event, make an action
# Startup event
@app.on_event("startup")
async def startup_db_client():
    app_settings = get_settings()
    
    app.mongodb_connection = AsyncIOMotorClient(app_settings.MONGODB_URL)
    app.mongodb_database = app.mongodb_connection[app_settings.MONGO_DATABASE]

# Shutdown event
@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_connection.close()

app.include_router(base.base_router)
