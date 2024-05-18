from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from app.schemas import LichLamViec
from app.models import LichLamViec as LichLamViecModel
from app.core.db import get_db
from app.crud.crud_schedule import get_lich_lam_viec, get_all_lich_lam_viec, get_lich_lam_viec_by_nhanvien
from app.crud.crud_request import get_phieu_thong_tin

router = APIRouter(tags=['LichLamViec'])

@router.get('/lichlamviec', response_model=list[LichLamViec])
async def read_all_lich_lam_viec(db = Depends(get_db)):
    try:
        dslv = get_all_lich_lam_viec(db)
        return dslv
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/lichlamviec/{id}', response_model=LichLamViec)
async def read_lich_lam_viec_id(IdLLV: str, db = Depends(get_db)):
    schedule = get_lich_lam_viec(db, IdLLV=IdLLV)
    
    if schedule is None:
        raise HTTPException(status_code=404, detail="Lich lam viec khong ton tai")
    return schedule

@router.get('/lichlamviec/nhanvien/{id}', response_model=list[LichLamViec])
async def read_lich_lam_viec_by_nhanvien(IdNV: str, db = Depends(get_db)):
    schedule = get_lich_lam_viec_by_nhanvien(db, IdNV=IdNV)
    
    if schedule is None:
        raise HTTPException(status_code=404, detail="Lich lam viec khong ton tai")
    return schedule

@router.post('/lichlamviec', response_model=LichLamViec)
async def create_lich_lam_viec(schedule: LichLamViec, db = Depends(get_db)):
    newSchedule = LichLamViecModel(IdLLV=schedule.IdLLV, IdNV=schedule.IdNV, TGBD=schedule.TGBD, TGKT=schedule.TGKT)
    db.add(newSchedule)
    db.commit()
    db.refresh(newSchedule)

    return schedule

@router.post('lichlamviec/{idPhieu}', response_model=LichLamViec)
async def create_lich_lam_viec_by_phieu(IdPhieu: str, db = Depends(get_db)):   
    phieu = get_phieu_thong_tin(db, IdPhieu)

    if phieu is None:
        raise HTTPException(status_code=404, detail="Phieu thong tin khong ton tai")
    
    for ct in phieu.ChiTiet:
        newSchedule = LichLamViecModel(IdNV=ct.IdNV, TGBD=phieu.TGBD, TGKT=phieu.TGKT)
        db.add(newSchedule)
        db.commit()
        db.refresh(newSchedule)

@router.delete('/lichlamviec/{id}', response_model=LichLamViec)
async def delete_lich_lam_viec(IdLLV: str, db = Depends(get_db)):
    schedule = get_lich_lam_viec(db, IdLLV=IdLLV)

    if schedule is None:
        raise HTTPException(status_code=404, detail="Lich lam viec khong ton tai")
    else:
        db.delete(schedule)
        db.commit()
        db.refresh(schedule)

        raise HTTPException(status_code=200, detail="Xoa lich lam viec thanh cong")