from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.core.db import get_db
from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_user, get_password_hash, verify_password
from app.schemas import Token
from fastapi import status

router = APIRouter(tags=['Master'])

@router.post('/token')
async def login_for_access_token(
    username: str, password: str, db = Depends(get_db)
) -> Token:
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.CCCD, "name": user.HoTen}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.get('/users/me')
async def read_users_me(current_user: Annotated[Token, Depends(get_current_user)]) -> Token:
    return current_user

@router.get('/test')
async def test(pwd: str, hash: str, db = Depends(get_db)) -> str:
    test = authenticate_user(db, pwd, hash)

    return test.HoTen