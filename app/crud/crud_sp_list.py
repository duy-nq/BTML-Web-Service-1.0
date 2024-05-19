from sqlalchemy.orm import Session
from app.models import DSLK

def get_all_lk(db: Session):
    return db.query(DSLK).all()

def get_lk(db: Session, IdDSLK: str):
    return db.query(DSLK).filter(DSLK.IdDSLK == IdDSLK).first()

def get_lk_by_baotri(db: Session, IdBT: str):
    return db.query(DSLK).filter(DSLK.IdBT == IdBT).all()