from fastapi import APIRouter

from app.api.v1.api_mechanic import router as nhanvien_router
from app.api.v1.api_login import router as login_router
from app.api.v1.api_customer import router as khachhang_router
from app.api.v1.api_schedule import router as lichhen_router
from app.api.v1.api_service import router as dichvu_router
from app.api.v1.api_ac import router as maylanh_router
from app.api.v1.api_request import router as phieuthongtin_router
from app.api.v1.api_sd import router as ctdv_router
from app.api.v1.api_sp import router as linhkien_router
from app.api.v1.api_sp_supplier import router as lkncc_router
from app.api.v1.api_supplier import router as nhacungcap_router
from app.api.v1.api_sp_list import router as dslk_router
from app.api.v1.api_maintenance import router as baotri_router
from app.api.v1.api_payment import router as thanhtoan_router
from app.api.v1.api_security import router as security_router
from app.api.v1.api_mail import router as mail_router

router = APIRouter(prefix='/v1')
router.include_router(login_router)
router.include_router(khachhang_router)
router.include_router(lichhen_router)
router.include_router(nhanvien_router)
router.include_router(dichvu_router)
router.include_router(phieuthongtin_router)
router.include_router(ctdv_router)
router.include_router(baotri_router)
router.include_router(dslk_router)
router.include_router(thanhtoan_router)
router.include_router(nhacungcap_router)
router.include_router(linhkien_router)
router.include_router(lkncc_router)
router.include_router(maylanh_router)
router.include_router(security_router)
router.include_router(mail_router)