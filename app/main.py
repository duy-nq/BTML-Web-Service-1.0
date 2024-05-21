from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models

from app.core.db import engine
from app.api import router as main_router

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    # Add other origins if needed
]

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(main_router)
