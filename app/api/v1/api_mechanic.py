from collections import defaultdict
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from app.crud.crud_customer import get_khach_hang
from app.crud.crud_request import get_phieu_thong_tin
from app.crud.crud_sd import get_ctdv_by_phieu
from app.crud.crud_service import get_dich_vu
from app.schemas import NhanVien, NhanVienSignUp, ResetPassword, UserPassword
from app.models import NhanVien as NhanVienModel
from app.core.db import get_db
from app.crud.crud_mechanic import get_all_nhan_vien, get_nhan_vien, get_nhan_vien_by_cccd, get_nhan_vien_by_gmail, get_password_by_id
from sqlalchemy.exc import IntegrityError
from app.core.config import settings

router = APIRouter(tags=['NhanVien'])

@router.get('/nhanvien', response_model=list[NhanVien])
async def read_nhan_vien(db = Depends(get_db)):
    try:
        dsnv = get_all_nhan_vien(db)
        return dsnv
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/nhanvien/{id}', response_model=NhanVien)
async def read_nhan_vien_id(IdNV: str, db = Depends(get_db)):
    nhanvien = get_nhan_vien(db, IdNV=IdNV)

    if nhanvien is None:
        raise HTTPException(status_code=404, detail="Nhan vien khong ton tai")
    return nhanvien

@router.get('/nhanvien/phieu/{id}')
async def read_nhan_vien_phieu(IdNV: str, db = Depends(get_db)):
    nhanvien = get_nhan_vien(db, IdNV=IdNV)

    if nhanvien is None:
        raise HTTPException(status_code=404, detail="Nhan vien khong ton tai")

    listOfRequest = []
    for request in nhanvien.service_detail:
        phieu = get_phieu_thong_tin(db, IdPhieu=request.IdPhieu)

        if phieu.TGBD != None and phieu.TGKT != None:
            continue
        
        listOfRequest.append(
            [
                request.IdPhieu, 
                phieu.LichHen, 
                get_dich_vu(db, request.IdDV).Ten,
                get_khach_hang(db, IdKH=phieu.IdKH).DiaChi,
            ]
        )

    idphieu_services = defaultdict(list)

    listOfRequest.sort(key=lambda x: x[1], reverse=False)

    # Iterate through the data and populate the defaultdict
    for item in listOfRequest:
        idphieu = item[0]
        thoi_gian = item[1]
        service = item[2]
        idphieu_services[idphieu].append(service)

    # Create a list to hold the final JSON objects
    final_data = []

    unique_idphieu = set()

    for item in listOfRequest:
        idphieu = item[0]
        # Check if IdPhieu is already processed
        if idphieu not in unique_idphieu:
            unique_idphieu.add(idphieu)
            services = idphieu_services[idphieu]
            thoi_gian = item[1]
            dia_chi = item[3]
            json_obj = {
                "IdPhieu": idphieu,
                "ListOfService": services,
                "ThoiGian": thoi_gian,
                "DiaChi": dia_chi
            }
            final_data.append(json_obj)

    return final_data

@router.post('/nhanvien/signup')
async def create_nhan_vien_singup(nhan_vien: NhanVienSignUp, db = Depends(get_db)):
    nhanvien = get_nhan_vien_by_gmail(db, Gmail=nhan_vien.Username)

    if nhanvien:
        return {"message": "Khach hang da ton tai"}
    
    newHash = settings.sha256_hash(nhan_vien.Password)
    
    try:
        newMechanic = NhanVienModel(HoTen=nhan_vien.HoTen, Gmail=nhan_vien.Username, MatKhau=newHash)
        db.add(newMechanic)
        db.commit()
        db.refresh(newMechanic)

        return {"message": "Dang ky thanh cong"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/nhanvien', response_model=NhanVien)
async def create_nhan_vien(nhan_vien: NhanVien, db = Depends(get_db)):
    nhanvien = get_nhan_vien_by_cccd(db, CCCD=nhan_vien.CCCD)

    if nhanvien:
        return {"message": "Nhan vien da ton tai"}
    
    try:
        newMechanic = NhanVienModel(IdNV=nhan_vien.IdNV, CCCD=nhan_vien.CCCD, HoTen=nhan_vien.HoTen, DiaChi=nhan_vien.DiaChi, SDT=nhan_vien.SDT, Gmail=nhan_vien.Gmail, DiemDG=nhan_vien.DiemDG, TrangThai=nhan_vien.TrangThai)
        db.add(newMechanic)
        db.commit()
        db.refresh(newMechanic)
        return nhan_vien
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put('/nhanvien/{id}', response_model=NhanVien)
async def update_nhan_vien(IdNV: str, nhan_vien: NhanVien, db = Depends(get_db)):
    try:
        nhanvien = get_nhan_vien(db, IdNV=IdNV)
        nhanvien.CCCD = nhan_vien.CCCD
        nhanvien.HoTen = nhan_vien.HoTen
        nhanvien.DiaChi = nhan_vien.DiaChi
        nhanvien.SDT = nhan_vien.SDT
        nhanvien.Gmail = nhan_vien.Gmail
        nhanvien.DiemDG = nhan_vien.DiemDG
        nhanvien.TrangThai = nhan_vien.TrangThai
        db.commit()
        return nhanvien
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put('/nhanvien/password/{id}')
async def update_khach_hang_password(IdNV: str, new_password: UserPassword, db = Depends(get_db)):
    old_password = get_password_by_id(db, IdNV=IdNV)

    nhanvien = get_nhan_vien(db, IdNV=IdNV)
    
    if old_password:
        if old_password != settings.sha256_hash(new_password.OldPassword):
            return {"message": "Mat khau cu khong dung"}
        newHash = settings.sha256_hash(new_password.NewPassword)
        nhanvien.MatKhau = newHash

        db.commit()
        db.refresh(nhanvien)
    else:
        return {"message": "Thao tac khong thanh cong"} 
    
    return {"message": "Doi mat khau thanh cong"}

@router.put('/nhanvien/reset/')
async def reset_nhan_vien_password(reset: ResetPassword, db = Depends(get_db)):
    nhanvien = get_nhan_vien_by_gmail(db, Gmail=reset.Email)
    
    if nhanvien:       
        newHash = settings.sha256_hash(reset.Password)
        nhanvien.MatKhau = newHash

        db.commit()
        db.refresh(nhanvien)
    else:
        raise HTTPException(status_code=404, detail="Nhan vien khong ton tai")
    
    return {"message": "Doi mat khau thanh cong"}
    
@router.delete('/nhanvien/{id}', response_model=NhanVien)
async def delete_nhan_vien(IdNV: str, db = Depends(get_db)):
    nhanvien = get_nhan_vien(db, IdNV=IdNV)

    if not nhanvien:
        raise HTTPException(status_code=404, detail="Nhan vien khong ton tai")
    else:
        if len(nhanvien.service_detail) != 0:
            raise HTTPException(status_code=400, detail="Nhan vien co lien ket voi dich vu, khong the xoa")
    try:
        db.delete(nhanvien)
        db.commit()
        raise HTTPException(status_code=200, detail="Xoa thanh cong")
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail=str(e))