from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from app.crud.crud_sd import get_ctdv
from app.schemas import BaoTri, BaoTriCreate, BaoTriForMechanic, BaoTriForUser
from app.models import BaoTri as BaoTriModel
from app.core.db import get_db
from app.crud.crud_maintenance import get_all_bt, get_bt, get_bt_by_ctdv

router = APIRouter(tags=['BaoTri'])

@router.get('/baotri', response_model=list[BaoTri])
async def read_all_bt(db = Depends(get_db)):
    try:
        baotri = get_all_bt(db)
        return baotri
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/baotri/{id}', response_model=BaoTri)
async def read_bt_id(IdBT: str, db = Depends(get_db)):
    baotri = get_bt(db, IdBT=IdBT)
    
    if baotri is None:
        raise HTTPException(status_code=404, detail="Bao tri khong ton tai")
    return baotri

@router.post('/baotri', response_model=BaoTri)
async def create_bt(maintenance: BaoTriCreate, db = Depends(get_db)):
    try:
        ac_qty = get_ctdv(db, IdCTDV=maintenance.IdCTDV).Soluong
        bt_qty = len(get_bt_by_ctdv(db, IdCTDV=maintenance.IdCTDV))
    except AttributeError:
        raise HTTPException(status_code=404, detail="Dich vu nay chua duoc tao hoac nhap sai id")

    if bt_qty >= ac_qty:
        raise HTTPException(status_code=400, detail="So lan bao tri da dat toi gioi han")
    
    try:
        baotri = BaoTriModel(IdCTDV = maintenance.IdCTDV, Serial = maintenance.Serial, DiemDG = maintenance.DiemDG)        
        db.add(baotri)
        db.commit()
        db.refresh(baotri)
        raise HTTPException(status_code=200, detail="Them bao tri thanh cong")
    except IntegrityError:
        raise HTTPException(status_code=500, detail="Them bao tri that bai")
    
@router.put('/baotri/serial/{id}', response_model=BaoTri)
async def update_bt_admin(id: str, maintenance: BaoTriForMechanic, db = Depends(get_db)):
    baotri = get_bt(db, IdBT=id)
    
    if baotri is None:
        raise HTTPException(status_code=404, detail="Bao tri khong ton tai")
    try:
        baotri.Serial = maintenance.Serial
        db.commit()
        db.refresh(baotri)

        raise HTTPException(status_code=200, detail="Cap nhat serial thanh cong")
    except IntegrityError:
        raise HTTPException(status_code=500, detail="Cap nhat serial that bai")
    
@router.put('/baotri/diem/{id}', response_model=BaoTri)
async def update_bt_user(id: str, maintenance: BaoTriForUser, db = Depends(get_db)):
    baotri = get_bt(db, IdBT=id)
    
    if baotri is None:
        raise HTTPException(status_code=404, detail="Bao tri khong ton tai")
    try:
        if (maintenance.DiemDG < 0) or (maintenance.DiemDG > 100):
            raise HTTPException(status_code=400, detail="Diem danh gia khong hop le")
        
        baotri.DiemDG = maintenance.DiemDG
        db.commit()
        db.refresh(baotri)

        raise HTTPException(status_code=200, detail="Cap nhat diem thanh cong")
    except IntegrityError:
        raise HTTPException(status_code=500, detail="Cap nhat diem that bai")
    
@router.delete('/baotri/{id}', response_model=BaoTri)
async def delete_bt(id: str, db = Depends(get_db)):
    baotri = get_bt(db, IdBT=id)
    
    if baotri is None:
        raise HTTPException(status_code=404, detail="Bao tri khong ton tai")
    try:
        db.delete(baotri)
        db.commit()
        raise HTTPException(status_code=200, detail="Xoa bao tri thanh cong")
    except IntegrityError:
        raise HTTPException(status_code=500, detail="Xoa bao tri that bai")
