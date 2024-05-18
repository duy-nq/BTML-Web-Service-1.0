from sqlalchemy.orm import Session
from app.models import PhieuThongTin

def get_all_phieu_thong_tin(db: Session):
    return db.query(PhieuThongTin).all()

def get_phieu_thong_tin(db: Session, IdPhieu: str):
    return db.query(PhieuThongTin).filter(PhieuThongTin.IdPhieu == IdPhieu).first()