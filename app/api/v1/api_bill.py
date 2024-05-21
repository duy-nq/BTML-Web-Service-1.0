from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from app.schemas import HoaDon, HoaDonCreate
from app.models import HoaDon as HDModel
from app.core.db import get_db
from app.crud.crud_bill import get_hd, get_all_hd, get_hd_by_phieu

router = APIRouter(tags=['HoaDon'])

@router.get('/hoadon', response_model=list[HoaDon])
async def read_all_hd(db = Depends(get_db)):
    try:
        dshd = get_all_hd(db)
        return dshd
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/hoadon/{id}', response_model=HoaDon)
async def read_hd_id(IdHD: str, db = Depends(get_db)):
    bill = get_hd(db, IdHD=IdHD)
    
    if bill is None:
        raise HTTPException(status_code=404, detail="Hoa don khong ton tai")
    return bill

@router.get('/hoadon/phieu/{id}', response_model=list[HoaDon])
async def read_hd_by_phieu(IdPhieu: str, db = Depends(get_db)):
    bill = get_hd_by_phieu(db, IdPhieu=IdPhieu)
    
    if bill is None:
        raise HTTPException(status_code=404, detail="Hoa don khong ton tai")
    return bill

@router.post('/hoadon', response_model=HoaDon)
async def create_hd(bill: HoaDonCreate, db = Depends(get_db)):
    newBill = HDModel(IdPhieu=bill.IdPhieu, ThanhTien=bill.ThanhTien, NoiDung=bill.NoiDung)
    try:
        db.add(newBill)
        db.commit() 
        db.refresh(newBill)

        return newBill
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail=str(e))
