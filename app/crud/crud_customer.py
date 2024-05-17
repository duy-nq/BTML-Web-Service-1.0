from sqlalchemy.orm import Session
from app.models import KhachHang

def get_all_khach_hang(db: Session):
    return db.query(KhachHang).all()

def get_khach_hang(db: Session, IdKH: str):
    return db.query(KhachHang).filter(KhachHang.IdKH == IdKH).first()