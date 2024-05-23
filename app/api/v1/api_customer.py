from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from app.crud.crud_ac import get_may_lanh
from app.crud.crud_maintenance import get_bt_by_ctdv
from app.schemas import KhachHang, KhachHangCreate, KhachHangHistory, ResetPassword, UserPassword
from app.models import KhachHang as KhachHangModel
from app.core.db import get_db
from app.crud.crud_customer import get_khach_hang, get_all_khach_hang, get_khach_hang_by_cccd, get_khach_hang_by_gmail, get_password_by_id
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

@router.get('/khachhang/history/{id}')
async def read_khach_hang_history(IdKH: str, db = Depends(get_db)):
    khachhang = get_khach_hang(db, IdKH=IdKH)
    
    if khachhang is None:
        raise HTTPException(status_code=404, detail="Khach hang khong ton tai")

    listOfRequest = []
    for request in khachhang.requests:
        listOfRequest.append(request)

    service_detail = []
    for request in listOfRequest:
        for detail in request.service_detail:
            service_detail.append(detail.IdCTDV)

    arr = []
    for id in service_detail:
        arr.append(get_bt_by_ctdv(db, IdCTDV=id))

    return arr


    






@router.post('/khachhang/signup')
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

@router.put('/khachhang/password/{id}')
async def update_khach_hang_password(IdKH: str, new_password: UserPassword, db = Depends(get_db)):
    old_password = get_password_by_id(db, IdKH=IdKH)

    khachhang = get_khach_hang(db, IdKH=IdKH)
    
    if old_password:
        if old_password != settings.sha256_hash(new_password.OldPassword):
            return {"message": "Mat khau cu khong dung"}
        newHash = settings.sha256_hash(new_password.NewPassword)
        khachhang.MatKhau = newHash

        db.commit()
        db.refresh(khachhang)
    else:
        return {"message": "Khach hang khong ton tai"}  

    return {"message": "Doi mat khau thanh cong"}

@router.put('/khachhang/reset/')
async def reset_khach_hang_password(reset: ResetPassword, db = Depends(get_db)):  
    khachhang = get_khach_hang_by_gmail(db, Gmail=reset.Email)
    
    if khachhang:
        newHash = settings.sha256_hash(reset.Password)
        khachhang.MatKhau = newHash

        db.commit()
        db.refresh(khachhang)
    else:
        raise HTTPException(status_code=404, detail="Khach hang khong ton tai")

    return {"message": "Reset mat khau thanh cong"}

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