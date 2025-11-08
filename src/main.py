from fastapi import FastAPI
# from routes.base import base_router
# from routes.data import data_router
from routes import base, data

app = FastAPI()
app.include_router(base.base_router)
app.include_router(data.data_router)
