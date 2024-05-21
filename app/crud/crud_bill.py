from sqlalchemy.orm import Session
from app.models import HoaDon

def get_all_hd(db: Session):
    return db.query(HoaDon).all()

def get_hd(db: Session, IdHD: str):
    return db.query(HoaDon).filter(HoaDon.IdHD == IdHD).first()

def get_hd_by_phieu(db: Session, IdPhieu: str):
    return db.query(HoaDon).filter(HoaDon.IdPhieu == IdPhieu).all()