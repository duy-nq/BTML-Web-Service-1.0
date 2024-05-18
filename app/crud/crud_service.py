from sqlalchemy.orm import Session
from app.models import DichVu

def get_all_dich_vu(db: Session):
    return db.query(DichVu).all()

def get_dich_vu(db: Session, IdDV: str):
    return db.query(DichVu).filter(DichVu.IdDV == IdDV).first()