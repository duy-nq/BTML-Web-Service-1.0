from sqlalchemy.orm import Session
from app.models import NhanVien

def get_all_nhan_vien(db: Session):
    return db.query(NhanVien).all()

def get_nhan_vien(db: Session, IdNV: str):
    return db.query(NhanVien).filter(NhanVien.IdNV == IdNV).first()

def get_nhan_vien_by_cccd(db: Session, CCCD: str):
    return db.query(NhanVien).filter(NhanVien.CCCD == CCCD).first()