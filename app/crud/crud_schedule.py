from sqlalchemy.orm import Session
from app.models import LichLamViec

def get_all_lich_lam_viec(db: Session):
    return db.query(LichLamViec).all()

def get_lich_lam_viec(db: Session, IdLLV: str):
    return db.query(LichLamViec).filter(LichLamViec.IdLLV == IdLLV).first()

def get_lich_lam_viec_by_nhanvien(db: Session, IdNV: str):
    return db.query(LichLamViec).filter(LichLamViec.IdNV == IdNV).all()

def create_lich_lam_viec(db: Session, IdNV: str):
    new_schedule = LichLamViec(IdNV = IdNV)
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule