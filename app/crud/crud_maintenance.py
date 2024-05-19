from sqlalchemy.orm import Session
from app.models import BaoTri

def get_all_bt(db: Session):
    return db.query(BaoTri).all()

def get_bt(db: Session, IdBT: str):
    return db.query(BaoTri).filter(BaoTri.IdBT == IdBT).first()

def get_bt_by_ctdv(db: Session, IdCTDV: str):
    return db.query(BaoTri).filter(BaoTri.IdCTDV == IdCTDV).all()