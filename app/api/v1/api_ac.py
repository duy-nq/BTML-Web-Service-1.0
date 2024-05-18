from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from app.schemas import MayLanh
from app.models import MayLanh as MayLanhModel
from app.core.db import get_db
from app.crud.crud_ac import get_may_lanh, get_all_may_lanh

router = APIRouter(tags=['MayLanh'])

@router.get('/maylanh', response_model=list[MayLanh])
async def read_all_may_lanh(db = Depends(get_db)):
    try:
        dsmaylanh = get_all_may_lanh(db)
        return dsmaylanh
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/maylanh/{id}', response_model=MayLanh)
async def read_may_lanh_id(IdML: str, db = Depends(get_db)):
    ac = get_may_lanh(db, IdML=IdML)
    
    if ac is None:
        raise HTTPException(status_code=404, detail="May lanh khong ton tai")
    return ac

@router.post('/maylanh', response_model=MayLanh)
async def create_may_lanh(ac: MayLanh, db = Depends(get_db)):
    newAC = MayLanhModel(IdML=ac.IdML, Ten=ac.Ten, Gia=ac.Gia, HangSX=ac.HangSX)
    db.add(newAC)
    db.commit()
    db.refresh(newAC)

    return ac

@router.put('/maylanh/{id}', response_model=MayLanh)
async def update_may_lanh(IdML: str, ac: MayLanh, db = Depends(get_db)):
    ac_old = get_may_lanh(db, IdML=IdML)

    if ac:
        ac_old.Ten = ac.Ten
        ac_old.IdCC = ac.IdCC

        db.commit()
        db.refresh(ac)
    else:
        return {"message": "May lanh khong ton tai"}    

    return ac

@router.delete('/maylanh/{id}', response_model=MayLanh)
async def delete_may_lanh(IdML: str, db = Depends(get_db)):
    ac = get_may_lanh(db, IdML=IdML)

    if ac is None:
        raise HTTPException(status_code=404, detail="May lanh khong ton tai")
    else:
        db.delete(ac)
        db.commit()
        db.refresh(ac)

        raise HTTPException(status_code=200, detail="Xoa may lanh thanh cong")