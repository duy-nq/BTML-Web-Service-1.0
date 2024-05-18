from sqlalchemy.orm import Session
from app.models import CTDV

def get_all_ctdv(db: Session):
    return db.query(CTDV).all()

def get_ctdv(db: Session, IdCTDV: str):
    return db.query(CTDV).filter(CTDV.IdCTDV == IdCTDV).first()

def get_ctdv_by_phieu(db: Session, IdPhieu: str):
    return db.query(CTDV).filter(CTDV.IdPhieu == IdPhieu).all()