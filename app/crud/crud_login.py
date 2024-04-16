from sqlalchemy.orm import Session
from sqlalchemy import text

def get_user_info(db: Session, gmail: str):
    SP_DANGNHAP = text('EXEC dbo.SP_DANGNHAP :gmail')

    result = db.execute(SP_DANGNHAP, {'gmail': gmail})

    info = result.fetchall()

    return {
        'Username': info[0][0],
        'HoTen': info[0][1],
        'TenNhom': info[0][2]
    }