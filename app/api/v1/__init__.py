from fastapi import APIRouter

from app.api.v1.api_mechanic import router as nhanvien_router

router = APIRouter(prefix='/v1')
router.include_router(nhanvien_router)