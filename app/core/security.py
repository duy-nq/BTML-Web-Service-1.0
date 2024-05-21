from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.db import get_db
from app.crud.crud_customer import get_khach_hang_by_gmail
from app.crud.crud_mechanic import get_nhan_vien_by_gmail
from app.models import NhanVien
from app.schemas import TokenData
from app.core.config import settings

SECRET_KEY = "3ec34d7a5a7cf24d7d72f8b63f659a055438d0ca283c178100fd579b8b634177"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return get_password_hash(plain_password) == hashed_password


def get_password_hash(password):
    return settings.sha256_hash(password)


def get_user(db, username: str):
    attempt1 = get_khach_hang_by_gmail(db, username)
    attempt2 = get_nhan_vien_by_gmail(db, username)

    if attempt1:
        return attempt1
    if attempt2:
        return attempt2
    
    return None


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.MatKhau):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str, db):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[NhanVien, Depends(get_current_user)],
):
    if not current_user.TrangThai:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user