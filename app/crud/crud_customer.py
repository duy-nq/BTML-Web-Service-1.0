from sqlalchemy.orm import Session
from app.models import KhachHang

def get_all_khach_hang(db: Session):
    return db.query(KhachHang).all()

def get_khach_hang(db: Session, IdKH: str):
    return db.query(KhachHang).filter(KhachHang.IdKH == IdKH).first()

def get_khach_hang_by_cccd(db: Session, CCCD: str):
    return db.query(KhachHang).filter(KhachHang.CCCD == CCCD).first()

def get_khach_hang_by_gmail(db: Session, Gmail: str):
    return db.query(KhachHang).filter(KhachHang.Gmail == Gmail).first()

def get_password_by_gmail(db: Session, Gmail: str):
    return db.query(KhachHang).filter(KhachHang.Gmail == Gmail).first().MatKhau

def get_password_by_id(db: Session, IdKH: str):
    return db.query(KhachHang).filter(KhachHang.IdKH == IdKH).first().MatKhau