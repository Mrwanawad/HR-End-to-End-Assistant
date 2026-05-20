import os
from config.config import get_settings
from fastapi import FastAPI
from routes.base import base_router
from routes.data import data_router
from controllers import DataController

# uvicorn main:app --reload

app = FastAPI(
    title= get_settings().APP_NAME,
    description= 'HireVision App', 
    version= get_settings().APP_VERSION
)






app.include_router( base_router )
app.include_router( data_router )