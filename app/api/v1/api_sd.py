from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from app.schemas import CTDV, CTDVCreate
from app.models import CTDV as CTModel
from app.core.db import get_db
from app.crud.crud_sd import get_ctdv, get_all_ctdv, get_ctdv_by_phieu

router = APIRouter(tags=['CTDV'])

@router.get('/ctdv', response_model=list[CTDV])
async def read_all_ctdv(db = Depends(get_db)):
    try:
        dsctdv = get_all_ctdv(db)
        return dsctdv
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/ctdv/{id}', response_model=CTDV)
async def read_ctdv_id(IdCTDV: str, db = Depends(get_db)):
    service = get_ctdv(db, IdCTDV=IdCTDV)
    
    if service is None:
        raise HTTPException(status_code=404, detail="CTDV khong ton tai")
    return service

@router.get('/ctdv/phieu/{id}', response_model=list[CTDV])
async def read_ctdv_by_phieu(IdPhieu: str, db = Depends(get_db)):
    service = get_ctdv_by_phieu(db, IdPhieu=IdPhieu)
    
    if service is None:
        raise HTTPException(status_code=404, detail="CTDV khong ton tai")
    return service

@router.post('/ctdv', response_model=CTDV)
async def create_ctdv(service: CTDVCreate, db = Depends(get_db)):
    newService = CTModel(IdPhieu=service.IdPhieu, IdDV=service.IdDV, IdML=service.IdML, Soluong=service.Soluong)
    db.add(newService)
    db.commit()
    db.refresh(newService)

    return newService