from sqlalchemy.orm import Session
from app.models import NhaCC

def get_all_ncc(db: Session):
    return db.query(NhaCC).all()

def get_ncc(db: Session, IdCC: str):
    return db.query(NhaCC).filter(NhaCC.IdCC == IdCC).first()