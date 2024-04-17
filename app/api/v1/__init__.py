from fastapi import APIRouter

from app.api.v1.api_mechanic import router as nhanvien_router
from app.api.v1.api_login import router as login_router
from app.api.v1.api_logout import router as logout_router
from app.api.v1.api_customer import router as khachhang_router

router = APIRouter(prefix='/v1')
router.include_router(nhanvien_router)
router.include_router(login_router)
router.include_router(logout_router)
router.include_router(khachhang_router)