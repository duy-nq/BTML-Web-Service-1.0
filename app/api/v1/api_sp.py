from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from app.schemas import LinhKien
from app.models import LinhKien as LKModel
from app.core.db import get_db
from app.crud.crud_sp import get_all_linh_kien, get_linh_kien

router = APIRouter(tags=['LinhKien'])

@router.get('/linhkien', response_model=list[LinhKien])
async def read_all_linh_kien(db = Depends(get_db)):
    try:
        dslk = get_all_linh_kien(db)
        return dslk
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/linhkien/{id}', response_model=LinhKien)
async def read_linh_kien_id(IdLK: str, db = Depends(get_db)):
    service = get_linh_kien(db, IdLK=IdLK)
    
    if service is None:
        raise HTTPException(status_code=404, detail="Linh kien khong ton tai")
    return service


