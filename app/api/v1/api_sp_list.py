from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from app.schemas import DSLK, DSLKCreate, DSLKForAdmin
from app.models import DSLK as DSLKModel
from app.core.db import get_db
from app.crud.crud_sp_list import get_all_lk, get_lk, get_lk_by_baotri

router = APIRouter(tags=['DSLK'])

@router.get('/dslk', response_model=list[DSLK])
async def read_all_lk(db = Depends(get_db)):
    try:
        dslk = get_all_lk(db)
        return dslk
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/dslk/{id}', response_model=DSLK)
async def read_lk_id(IdLK: str, db = Depends(get_db)):
    linhkien = get_lk(db, IdLK=IdLK)
    
    if linhkien is None:
        raise HTTPException(status_code=404, detail="Linh kien khong ton tai")
    return linhkien

@router.post('/dslk', response_model=DSLK)
async def create_lk(sp_list: DSLKCreate, db = Depends(get_db)):
    try:
        linhkien = DSLKModel(IdBT = sp_list.IdBT, IdLKCC = sp_list.IdLKCC, SoLuong = sp_list.SoLuong)
        db.add(linhkien)
        db.commit()
        db.refresh(linhkien)
        raise HTTPException(status_code=200, detail="Them linh kien vao danh sach thanh cong")
    except IntegrityError:
        raise HTTPException(status_code=500, detail="Them linh kien vao danh sach that bai, kiem tra lai thong tin nhap vao")
    
@router.put('/dslk/{id}', response_model=DSLK)
async def update_lk(id: str, sp_list: DSLKForAdmin, db = Depends(get_db)):
    linhkien = get_lk(db, IdDSLK=id)
    
    if linhkien is None:
        raise HTTPException(status_code=404, detail="Linh kien khong ton tai")
    try:
        linhkien.IdLKCC = sp_list.IdLKCC
        linhkien.SoLuong = sp_list.SoLuong
        db.commit()
        db.refresh(linhkien)

        raise HTTPException(status_code=200, detail="Cap nhat linh kien thanh cong")
    except IntegrityError:
        raise HTTPException(status_code=500, detail="Cap nhat linh kien that bai")
    
@router.delete('/dslk/{id}')
async def delete_lk(id: str, db = Depends(get_db)):
    linhkien = get_lk(db, IdDSLK=id)
    
    if linhkien is None:
        raise HTTPException(status_code=404, detail="Linh kien khong ton tai")
    try:
        db.delete(linhkien)
        db.commit()
        raise HTTPException(status_code=200, detail="Xoa linh kien thanh cong")
    except IntegrityError:
        raise HTTPException(status_code=500, detail="Xoa linh kien that bai")
