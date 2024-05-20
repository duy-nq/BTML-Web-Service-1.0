from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from app.schemas import KhachHang, KhachHangCreate
from app.models import KhachHang as KhachHangModel
from app.core.db import get_db
from app.crud.crud_customer import get_khach_hang, get_all_khach_hang, get_khach_hang_by_cccd, get_khach_hang_by_gmail
from app.core.config import settings

router = APIRouter(tags=['KhachHang'])

@router.get('/khachhang', response_model=list[KhachHang])
async def read_all_khach_hang(db = Depends(get_db)):
    try:
        dskh = get_all_khach_hang(db)
        return dskh
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/khachhang/{id}', response_model=KhachHang)
async def read_khach_hang_id(IdKH: str, db = Depends(get_db)):
    khachhang = get_khach_hang(db, IdKH=IdKH)
    
    if khachhang is None:
        raise HTTPException(status_code=404, detail="Khach hang khong ton tai")
    return khachhang

@router.post('/khachhang/singup')
async def create_khach_hang_singup(khach_hang: KhachHangCreate, db = Depends(get_db)):
    khachhang = get_khach_hang_by_gmail(db, Gmail=khach_hang.Username)

    if khachhang:
        return {"message": "Khach hang da ton tai"}
    
    newHash = settings.sha256_hash(khach_hang.Password)
    
    try:
        newCustomer = KhachHangModel(HoTen=khach_hang.HoTen, Gmail=khach_hang.Username, MatKhau=newHash)
        db.add(newCustomer)
        db.commit()
        db.refresh(newCustomer)

        return {"message": "Dang ky thanh cong"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/khachhang', response_model=KhachHang)
async def create_khach_hang(khach_hang: KhachHang, db = Depends(get_db)):
    khachhang = get_khach_hang_by_cccd(db, CCCD=khach_hang.CCCD)

    if khachhang:
        return {"message": "Khach hang da ton tai"}
    
    newCustomer = KhachHangModel(IdKH=khach_hang.IdKH, CCCD=khach_hang.CCCD, HoTen=khach_hang.HoTen, DiaChi=khach_hang.DiaChi, SDT=khach_hang.SDT, Gmail=khach_hang.Gmail)
    db.add(newCustomer)
    db.commit()
    db.refresh(newCustomer)

    return khach_hang

@router.put('/khachhang/{id}', response_model=KhachHang)
async def update_khach_hang(IdKH: str, khach_hang: KhachHang, db = Depends(get_db)):
    khachhang = get_khach_hang(db, IdKH=IdKH)

    if khachhang:
        khachhang.CCCD = khach_hang.CCCD
        khachhang.HoTen = khach_hang.HoTen
        khachhang.DiaChi = khach_hang.DiaChi
        khachhang.SDT = khach_hang.SDT
        khachhang.Gmail = khach_hang.Gmail

        db.commit()
        db.refresh(khachhang)
    else:
        return {"message": "Khach hang khong ton tai"}    

    return khach_hang

@router.delete('/khachhang/{id}', response_model=KhachHang)
async def delete_khach_hang(IdKH: str, db = Depends(get_db)):
    khachhang = get_khach_hang(db, IdKH=IdKH)

    if not khachhang:
        raise HTTPException(status_code=404, detail="Khach hang khong ton tai")
    
    try:
        db.delete(khachhang)
        db.commit()
        return {"message": "Xoa thanh cong"}
    except IntegrityError as e:
        raise HTTPException(status_code=404, detail="Khach hang dang duoc su dung")