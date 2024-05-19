from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from app.schemas import NhaCungCap
from app.core.db import get_db
from app.crud.crud_supplier import get_all_ncc, get_ncc

router = APIRouter(tags=['NhaCungCap'])

@router.get('/ncc', response_model=list[NhaCungCap])
async def read_all_ncc(db = Depends(get_db)):
    try:
        dsncc = get_all_ncc(db)
        return dsncc
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/ncc/{id}', response_model=NhaCungCap)
async def read_ncc_id(IdCC: str, db = Depends(get_db)):
    ncc = get_ncc(db, IdCC=IdCC)
    
    if ncc is None:
        raise HTTPException(status_code=404, detail="Nha cung cap khong ton tai")
    return ncc
