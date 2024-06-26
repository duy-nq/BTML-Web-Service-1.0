import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from app.crud.crud_ac import get_may_lanh
from app.crud.crud_service import get_dich_vu
from app.schemas import PhieuThongTin, PhieuThongTinCreate, TimeBase
from app.models import PhieuThongTin as PhieuThongTinModel
from app.core.db import get_db
from app.crud.crud_request import get_phieu_thong_tin, get_all_phieu_thong_tin

router = APIRouter(tags=['PhieuThongTin'])

@router.get('/phieuthongtin', response_model=list[PhieuThongTin])
async def read_all_phieu_thong_tin(db = Depends(get_db)):
    try:
        dsptt = get_all_phieu_thong_tin(db)
        return dsptt
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/phieuthongtin/{id}', response_model=PhieuThongTin)
async def read_phieu_thong_tin_id(IdPhieu: str, db = Depends(get_db)):
    request = get_phieu_thong_tin(db, IdPhieu=IdPhieu)
    
    if request is None:
        raise HTTPException(status_code=404, detail="Phieu thong tin khong ton tai")
    return request

@router.get('/phieuthongtin/chitiet/{id}')
async def read_phieu_thong_tin_chitiet(IdPhieu: str, db = Depends(get_db)):
    request = get_phieu_thong_tin(db, IdPhieu=IdPhieu)
    
    if request is None:
        raise HTTPException(status_code=404, detail="Phieu thong tin khong ton tai")
    
    listOfSD = []
    for sd in request.service_detail:
        listOfSD.append({
            'IdCT': sd.IdCTDV,
            'LoaiDV': get_dich_vu(db, IdDV=sd.IdDV).Ten,
            'LoaiML': get_may_lanh(db, IdML=sd.IdML).Ten,
            'SoLuong': sd.SoLuong
        })

    return listOfSD

@router.post('/phieuthongtin', response_model=PhieuThongTin)
async def create_phieu_thong_tin(request: PhieuThongTinCreate, db = Depends(get_db)):
    newRequest = PhieuThongTinModel(LichHen=request.LichHen, IdKH=request.IdKH, TrangThai=request.TrangThai)
    db.add(newRequest)
    db.commit()
    db.refresh(newRequest)

    return newRequest

@router.delete('/phieuthongtin/{id}')
async def delete_phieu_thong_tin(IdPhieu: str, db = Depends(get_db)):
    request = get_phieu_thong_tin(db, IdPhieu=IdPhieu)

    if request is None:
        raise HTTPException(status_code=404, detail="Phieu thong tin khong ton tai")
    else:
        db.delete(request)
        db.commit()

        raise HTTPException(status_code=200, detail="Xoa phieu thong tin thanh cong")
    
@router.put('/phieuthongtin/{id}', response_model=PhieuThongTin)
async def update_phieu_thong_tin(IdPhieu: str, request: PhieuThongTin, db = Depends(get_db)):
    oldRequest = get_phieu_thong_tin(db, IdPhieu=IdPhieu)

    if oldRequest is None:
        raise HTTPException(status_code=404, detail="Phieu thong tin khong ton tai")
    else:
        oldRequest.LichHen = request.LichHen
        oldRequest.TGBD = request.TGBD
        oldRequest.TGKT = request.TGKT
        oldRequest.IdKH = request.IdKH
        oldRequest.TrangThai = request.TrangThai

        db.commit()
        db.refresh(oldRequest)

        raise HTTPException(status_code=200, detail="Cap nhat phieu thong tin thanh cong")
    
@router.put('/phieuthongtin/thoigian/{id}')
async def update_phieu_thong_tin_thoigian(IdPhieu: str, request: TimeBase, db = Depends(get_db)):
    oldRequest = get_phieu_thong_tin(db, IdPhieu=IdPhieu)

    if oldRequest is None:
        raise HTTPException(status_code=404, detail="Phieu thong tin khong ton tai")
    else:
        oldRequest.TGBD = request.TGBD
        oldRequest.TGKT = request.TGKT

        db.commit()
        db.refresh(oldRequest)

        return {"message": "Cap nhat thoi gian thanh cong"}