from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional
from decimal import Decimal
from uuid import UUID

# Base class for both KhachHang and NhanVien
class UserBase(BaseModel):
    CCCD: Optional[str]
    HoTen: str
    DiaChi: Optional[str]
    SDT: Optional[str]
    Gmail: str

class TimeBase(BaseModel):
    TGBD: Optional[datetime]
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

class DSLKCreate(BaseModel):
    IdBT: UUID
    IdLKCC: UUID
    SoLuong: int

class DSLKForAdmin(BaseModel):
    IdLKCC: UUID
    SoLuong: int

class DSLK(DSLKCreate):
    IdDSLK: UUID
    IdBT: UUID
    IdLKCC: UUID
    SoLuong: int

    class Config:
        orm_mode = True

class LichLamViecCreate(TimeBase):
    IdNV: UUID

class LichLamViec(LichLamViecCreate):
    IdLLV: UUID

    class Config:
        orm_mode = True

class BaoTriCreate(BaseModel):
    IdCTDV: UUID
    Serial: str
    DiemDG: int

class BaoTriForMechanic(BaseModel):
    Serial: str

class BaoTriForUser(BaseModel):
    DiemDG: int

class BaoTri(BaoTriCreate):
    IdBT: UUID

    sp_list: list[DSLK] = []

    class Config:
        orm_mode = True

class CTDVCreate(BaseModel):
    IdPhieu: UUID
    IdML: UUID
    IdDV: UUID
    SoLuong: int

class CTDVForAdmin(BaseModel):
    IdNV: UUID

class CTDVForUser(BaseModel):
    IdML: UUID
    IdDV: UUID
    SoLuong: int

class CTDV(CTDVCreate):
    IdCTDV: UUID
    IdNV: Optional[UUID]

    maintenance: list[BaoTri] = []

    class Config:
        orm_mode = True

class NhanVienLogin(BaseModel):
    Username: str
    Password: str  

class NhanVienSignUp(NhanVienLogin):
    HoTen: str

class NhanVienCreate(UserBase):
    DiemDG: int
    TrangThai: bool

class NhanVien(NhanVienCreate):
    IdNV: UUID

    schedules: list[LichLamViec] = []
    service_detail: list[CTDV] = []

    class Config:
        orm_mode = True   

class HoaDonCreate(BaseModel):
    IdPhieu: UUID
    ThanhTien: Decimal = Field(..., alias='ThanhTien')
    NoiDung: str

class HoaDon(HoaDonCreate):
    IdHD: UUID
    ThoiGian: datetime

    class Config:
        json_encoder = {Decimal: float}
        orm_mode = True 

class PhieuThongTinCreate(BaseModel):
    IdKH: UUID
    LichHen: Optional[datetime]
    TrangThai: bool

    class Config:
        orm_mode = True

class PhieuThongTin(TimeBase):
    IdPhieu: UUID
    IdKH: UUID
    LichHen: Optional[datetime]
    TrangThai: bool

    service_detail: list[CTDV] = []
    bill: list[HoaDon] = []

    class Config:
        orm_mode = True

class KhachHangLogin(BaseModel):
    Username: str
    Password: str

class KhachHangCreate(KhachHangLogin):
    HoTen: str

class UserPassword(BaseModel):
    OldPassword: str
    NewPassword: str

class KhachHang(UserBase):
    IdKH: UUID

    requests: list[PhieuThongTin] = []

    class Config:
        orm_mode = True

class MayLanh(BaseModel):
    IdML: UUID
    Ten: str
    IdCC: UUID

    class Config:
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
    MoTa: Optional[str]
    HinhAnh: Optional[str]

    price_history: list[LSG_DV] = []

    class Config:
        json_encoder = {Decimal: float}
        orm_mode = True

class TongTienBase(BaseModel):
    Ten: str
    DonGia: Decimal = Field(..., alias='DonGia')
    SoLuong: int
    TongTien: Decimal = Field(..., alias='TongTien')

class TongTienDV(TongTienBase):
    IdDV: UUID

    class Config:
        json_encoder = {Decimal: float}
        orm_mode = True

class TongTienLK(TongTienBase):
    IdLK: UUID

    class Config:
        json_encoder = {Decimal: float}
        orm_mode = True

class requestData(BaseModel):
    vnp_Version:str
    vnp_Command:str
    vnp_TmnCode:str
    vnp_Amount:str
    vnp_CurrCode:str
    vnp_TxnRef:str
    vnp_OrderInfo:str
    vnp_OrderType:str
    vnp_Locale:str
    vnp_BankCode:Optional[str]=None
    vnp_CreateDate:str = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp_IpAddr:str
    vnp_ReturnUrl:Optional[str]=None

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class NhanVienInDB(NhanVien):
    hashed_password: str

class KhachHangInDB(KhachHang):
    hashed_password: str

class EmailSchema(BaseModel):
    email: List[EmailStr]

class Payment(BaseModel):
    IdPhieu: str
    ThanhTien: Decimal
    NoiDung: str

class ResetPassword(BaseModel):
    Email: str
    Password: str