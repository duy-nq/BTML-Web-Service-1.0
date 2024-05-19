from sqlalchemy.orm import Session
from app.models import LinhKien

def get_all_linh_kien(db: Session):
    return db.query(LinhKien).all()

def get_linh_kien(db: Session, IdLK: str):
    return db.query(LinhKien).filter(LinhKien.IdLK == IdLK).first()