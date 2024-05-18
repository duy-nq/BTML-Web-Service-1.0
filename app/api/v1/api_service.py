from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from app.schemas import DichVu as Service
from app.models import DichVu as ServiceModel
from app.core.db import get_db
from app.crud.crud_service import get_dich_vu, get_all_dich_vu

router = APIRouter(tags=['DichVu'])

@router.get('/dichvu', response_model=list[Service])
async def read_all_dich_vu(db = Depends(get_db)):
    try:
        dsdv = get_all_dich_vu(db)
        return dsdv
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/dichvu/{id}', response_model=Service)
async def read_dich_vu_id(IdDV: str, db = Depends(get_db)):
    service = get_dich_vu(db, IdDV=IdDV)
    
    if service is None:
        raise HTTPException(status_code=404, detail="Dich vu khong ton tai")
    return service

@router.post('/dichvu', response_model=Service)
async def create_dich_vu(service: Service, db = Depends(get_db)):
    newService = ServiceModel(IdDV=service.IdDV, Ten=service.Ten)
    db.add(newService)
    db.commit()
    db.refresh(newService)

    return service

@router.delete('/dichvu/{id}', response_model=Service)
async def delete_dich_vu(IdDV: str, db = Depends(get_db)):
    service = get_dich_vu(db, IdDV=IdDV)

    if service is None:
        raise HTTPException(status_code=404, detail="Dich vu khong ton tai")
    else:
        db.delete(service)
        db.commit()
        db.refresh(service)

        raise HTTPException(status_code=200, detail="Xoa dich vu thanh cong")