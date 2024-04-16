from fastapi import APIRouter
from app.core.config import settings
from app import models
from app.core.db import engine
from sqlalchemy import create_engine


router = APIRouter(tags=['Logout'])

@router.get('/logout')
async def logout():
    settings.username = settings.DEFAULT_USERNAME
    settings.password = settings.DEFAULT_PWD
    settings.role = ''
    settings.user_id = ''

    engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
    
    return {'msg': 'Logout successfully!'}