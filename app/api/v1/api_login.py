from fastapi import APIRouter, Depends
from app.schemas import InfoBase
from app.core.db import get_db
from app.crud.crud_login import get_user_info
from app.core.config import settings
from app.core.db import engine
from sqlalchemy import create_engine



router = APIRouter(tags=['Login'])

@router.get('/login')
async def login(gmail: str, password: str, db = Depends(get_db)):
    try:
        settings.username = gmail
        settings.pwd = password

        sqlalchemy_database_url = f'mssql+pyodbc://{settings.username}:{settings.pwd}@{settings.SERVER}/{settings.DATABASE}?driver={settings.DRIVER}'

        engine = create_engine(sqlalchemy_database_url)
        engine.connect()
        print(sqlalchemy_database_url)

        info = get_user_info(db, gmail)

        settings.user_id = info.get('Username')
        settings.role = info.get('TenNhom')

        print(settings.user_id, settings.role)
    except:
        settings.username = settings.DEFAULT_USERNAME
        settings.password = settings.DEFAULT_PWD
        settings.role = ''
        settings.user_id = ''
        
        return {'msg': 'Wrong username or password!'}

    return {'msg': 'Login successfully!'}

@router.get('/current', response_model=InfoBase)
async def read_info(db = Depends(get_db)):
    try:
        info = get_user_info(db, settings.username)
    except:
        return {
            'Username': 'master',
            'HoTen': 'master',
            'TenNhom': 'master'
        }

    return info