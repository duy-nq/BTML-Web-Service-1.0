from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from app.crud.crud_sp import get_linh_kien
from app.schemas import LK_NCC
from app.core.db import get_db
from app.crud.crud_sp_supplier import get_all_lk_ncc, get_lk_ncc

router = APIRouter(tags=['LK_NCC'])

@router.get('/lk_ncc', response_model=list[LK_NCC])
async def read_all_lk_ncc(db = Depends(get_db)):
    try:
        dslk = get_all_lk_ncc(db)
        return dslk
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/lk_ncc/chitiet')
async def read_lk_ncc_chitiet(db = Depends(get_db)):
    try:
        dslk = get_all_lk_ncc(db)

        listCopy = []

        for lk in dslk:
            listCopy.append({
                "IdLKCC": lk.IdLKCC,
                "IdLK": lk.IdLK,
                "IdCC": lk.IdCC,
                "Ten": get_linh_kien(db, IdLK=lk.IdLK).Ten,
            })

        return listCopy
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/lk_ncc/{id}', response_model=LK_NCC)
async def read_lk_ncc_id(IdLKCC: str, db = Depends(get_db)):
    linhkien = get_lk_ncc(db, IdLKCC=IdLKCC)
    
    if linhkien is None:
        raise HTTPException(status_code=404, detail="Linh kien khong ton tai")
    return linhkien

