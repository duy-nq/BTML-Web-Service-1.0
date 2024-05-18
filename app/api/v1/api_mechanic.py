from fastapi import APIRouter, Depends, HTTPException
from app.schemas import NhanVien
from app.models import NhanVien as NhanVienModel
from app.core.db import get_db
from app.crud.crud_mechanic import get_all_nhan_vien, get_nhan_vien, get_nhan_vien_by_cccd
from sqlalchemy.exc import IntegrityError

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
    # try:
    #     nhan_vien = get_nhan_vien(db, IdNV=IdNV)
    #     return nhan_vien
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

    nhanvien = get_nhan_vien(db, IdNV=IdNV)

    if nhanvien is None:
        raise HTTPException(status_code=404, detail="Nhan vien khong ton tai")
    return nhanvien

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