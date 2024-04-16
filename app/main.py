from fastapi import FastAPI
from app import models

from app.core.db import engine
from app.api import router as main_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(main_router)
