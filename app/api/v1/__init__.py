from fastapi import APIRouter

from app.api.v1.api_mechanic import router as nhanvien_router
from app.api.v1.api_login import router as login_router
from app.api.v1.api_logout import router as logout_router
from app.api.v1.api_customer import router as khachhang_router
from app.api.v1.api_schedule import router as lichhen_router
from app.api.v1.api_service import router as dichvu_router
from app.api.v1.api_ac import router as maylanh_router
from app.api.v1.api_request import router as phieuthongtin_router
from app.api.v1.api_sd import router as ctdv_router

router = APIRouter(prefix='/v1')
router.include_router(nhanvien_router)
router.include_router(login_router)
router.include_router(logout_router)
router.include_router(khachhang_router)
router.include_router(lichhen_router)
router.include_router(dichvu_router)
router.include_router(maylanh_router)
router.include_router(phieuthongtin_router)
router.include_router(ctdv_router)