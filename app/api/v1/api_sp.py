from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from app.schemas import LinhKien
from app.models import LinhKien as LKModel
from app.core.db import get_db
from app.crud.crud_sp import get_all_linh_kien, get_linh_kien