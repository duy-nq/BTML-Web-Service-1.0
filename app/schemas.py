from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal
from uuid import UUID

# Base class for both KhachHang and NhanVien
class UserBase(BaseModel):
    CCCD: str
    HoTen: str
    DiaChi: str
    SDT: str
    Gmail: str

class TimeBase(BaseModel):
    TGBD: datetime
    TGKT: Optional[datetime]

class InfoBase(BaseModel):
    Username: str
    HoTen: str = Field(default='master')
    TenNhom: str = Field(default='db_owner')

class PriceBase(BaseModel):
    ThoiGian: datetime
    DonGia: Decimal = Field(..., alias='DonGia')

class LSG_LK(PriceBase):
    IdLKCC: UUID

    class Config:
        json_encoder = {Decimal: float}
        orm_mode = True    

class LK_NCC(BaseModel):
    IdLKCC: UUID
    IdLK: UUID
    IdCC: UUID
    DonGia: Optional[Decimal] = Field(..., alias='DonGia')

    price_history: list[LSG_LK] = []

    class Config:
        json_encoder = {Decimal: float}
        orm_mode = True

class DSLK(BaseModel):
    IdDSLK: UUID
    IdBT: UUID
    IdLKCC: UUID
    SoLuong: int

    class Config:
        orm_mode = True

class PhanHoi(BaseModel):
    IdPH: UUID
    NoiDung: str
    IdBT: UUID

    class Config:
        orm_mode = True

class BaoTri(BaseModel):
    IdBT: UUID
    IdDSNV: UUID
    IdDSML: UUID
    DiemDG: int

    sp_list: list[DSLK] = []
    feedback: list[PhanHoi] = []

    class Config:
        orm_mode = True

class DSNV(BaseModel):
    IdDSNV: UUID
    IdCTDV: UUID
    IdNV: UUID

    class Config:
        orm_mode = True 

class ML_KH(BaseModel):
    IdMLKH: UUID
    IdML: UUID
    IdKH: UUID
    MaSo: int

    class Config:
        orm_mode = True 

class DSML(BaseModel):
    IdDSML: UUID
    IdCTDV: UUID
    IdMLKH: UUID

    customer_ac: list[ML_KH] = []

    class Config:
        orm_mode = True

class CTDV(BaseModel):
    IdCTDV: UUID
    IdPhieu: UUID
    IdML: UUID
    IdDV: UUID
    Soluong: int
    TrangThai: bool

    mechanics: list[DSNV] = []
    ac_list: DSML

    class Config:
        orm_mode = True       

class PhieuThongTin(TimeBase):
    IdPTT: UUID
    IdKH: UUID
    LichHen: Optional[datetime]
    TrangThai: bool

    service_detail: list[CTDV] = []

    class Config:
        orm_mode = True

class LichLamViec(TimeBase):
    IdLLV: UUID
    IdNV: UUID

    class Config:
        orm_mode = True

class KhachHang(UserBase):
    IdKH: UUID

    requests: list[PhieuThongTin] = []
    customer_ac: list[ML_KH] = []

    class Config:
        orm_mode = True

class NhanVien(UserBase):
    IdNV: UUID
    DiemDG: int
    TrangThai: bool

    schedules: list[LichLamViec] = []

    class Config:
        orm_mode = True

class MayLanh(BaseModel):
    IdML: UUID
    Ten: str
    DonGia: Decimal = Field(..., alias='DonGia')

    class Config:
        json_encoder = {Decimal: float}
        orm_mode = True

class LinhKien(BaseModel):
    IdLK: UUID
    Ten: str

    class Config:
        orm_mode = True

class NhaCungCap(BaseModel):
    IdCC: UUID
    Ten: str

    ac_list: list[MayLanh] = []

    class Config:
        orm_mode = True    

class LSG_DV(PriceBase):
    IdDV: UUID
    
    class Config:
        json_encoder = {Decimal: float}
        orm_mode = True    

class DichVu(BaseModel):
    IdDV: UUID
    Ten: str
    DonGia: Decimal = Field(..., alias='DonGia')
    KhoiLuong: float

    price_history: list[LSG_DV] = []

    class Config:
        json_encoder = {Decimal: float}
        orm_mode = True