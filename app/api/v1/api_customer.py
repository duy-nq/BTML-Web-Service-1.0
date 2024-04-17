from fastapi import APIRouter, Depends
from app.schemas import KhachHang
from app.core.db import get_db
from app.crud.crud_customer import get_khach_hang, get_all_khach_hang
from app.core.config import settings

router = APIRouter(tags=['KhachHang'])

@router.get('/khachhang', response_model=list[KhachHang])
async def read_all_khach_hang(db = Depends(get_db)):
    dskh = get_all_khach_hang(db)

    return dskh

@router.get('/khachhang/{id}', response_model=KhachHang)
async def read_khach_hang_id(IdKH: str, db = Depends(get_db)):
    khachhang = get_khach_hang(db, IdKH=IdKH)

    return khachhang

@router.get('/whoami', response_model=KhachHang)
async def read_khach_hang_current(db = Depends(get_db)):
    try:
        khach_hang = get_khach_hang(db, IdNV=settings.user_id)
    except:
        return {
            "CCCD": "undefined",
            "HoTen": "undefined",
            "DiaChi": "undefined",
            "SDT": "undefined",
            "Gmail": "undefined",
            "IdKH": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "request": [],
            "customer_ac": []
        }

    return khach_hang
