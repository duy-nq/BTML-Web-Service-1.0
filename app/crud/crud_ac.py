from sqlalchemy.orm import Session
from app.models import MayLanh

def get_all_may_lanh(db: Session):
    return db.query(MayLanh).all()

def get_may_lanh(db: Session, IdML: str):
    return db.query(MayLanh).filter(MayLanh.IdML == IdML).first()

def create_may_lanh(db: Session, IdML: str):
    new_maylanh = MayLanh(IdML = IdML)
    db.add(new_maylanh)
    db.commit()
    db.refresh(new_maylanh)
    return new_maylanh