from sqlalchemy.orm import Session
from app.models import LK_NCC

def get_all_lk_ncc(db: Session):
    return db.query(LK_NCC).all()

def get_lk_ncc(db: Session, IdLKCC: str):
    return db.query(LK_NCC).filter(LK_NCC.IdLKCC == IdLKCC).first()

def get_lk_ncc_by_ncc(db: Session, IdCC: str):
    return db.query(LK_NCC).filter(LK_NCC.IdCC == IdCC).all()