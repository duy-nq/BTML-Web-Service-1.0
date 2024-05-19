from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from app.schemas import CTDV, CTDVCreate, CTDVForAdmin
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

@router.post('/ctdv', response_model=CTDV)
async def create_ctdv(service: CTDVCreate, db = Depends(get_db)):
    newService = CTModel(IdPhieu=service.IdPhieu, IdDV=service.IdDV, IdML=service.IdML, Soluong=service.Soluong)
    db.add(newService)
    db.commit()
    db.refresh(newService)

    return newService

@router.put('/ctdv/{id}', response_model=CTDV)
async def update_ctdv(IdCTDV: str, service: CTDVForAdmin, db = Depends(get_db)):
    oldService = get_ctdv(db, IdCTDV=IdCTDV)
    
    if oldService is None:
        raise HTTPException(status_code=404, detail="CTDV khong ton tai")
    
    try:
        oldService.IdNV = service.IdNV
        db.commit()
        db.refresh(oldService)

        raise HTTPException(status_code=200, detail="Update thanh cong")
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail=str(e))