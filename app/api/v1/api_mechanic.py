from fastapi import APIRouter, Depends
from app.schemas import NhanVien
from app.core.db import get_db
from app.crud.crud_mechanic import get_all_nhan_vien, get_nhan_vien

router = APIRouter(tags=['NhanVien'])

@router.get('/nhanvien', response_model=list[NhanVien])
async def read_nhan_vien(db = Depends(get_db)):
    dsnv = get_all_nhan_vien(db)

    return dsnv

@router.get('/nhanvien/{id}', response_model=NhanVien)
async def read_nhan_vien_id(IdNV: int, db = Depends(get_db)):
    nhan_vien = get_nhan_vien(db, IdNV)

    return nhan_vien