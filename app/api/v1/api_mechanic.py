from fastapi import APIRouter, Depends
from app.schemas import NhanVien
from app.core.db import get_db
from app.crud.crud_mechanic import get_all_nhan_vien, get_nhan_vien
from app.core.config import settings

router = APIRouter(tags=['NhanVien'])

@router.get('/nhanvien', response_model=list[NhanVien])
async def read_nhan_vien(db = Depends(get_db)):
    dsnv = get_all_nhan_vien(db)

    return dsnv

@router.get('/nhanvien/{id}', response_model=NhanVien)
async def read_nhan_vien_id(IdNV: str, db = Depends(get_db)):
    nhan_vien = get_nhan_vien(db, IdNV)

    return nhan_vien

@router.get('/whoami', response_model=NhanVien)
async def read_nhan_vien_current(db = Depends(get_db)):
    try:
        nhan_vien = get_nhan_vien(db, IdNV=settings.user_id)
    except:
        return {
            "CCCD": "undefined",
            "HoTen": "undefined",
            "DiaChi": "undefined",
            "SDT": "undefined",
            "Gmail": "undefined",
            "IdNV": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "DiemDG": 0,
            "TrangThai": True,
            "schedules": []
        }

    return nhan_vien