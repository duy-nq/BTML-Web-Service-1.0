from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.dialects.mssql import MONEY, DATETIME, UNIQUEIDENTIFIER as UUID
from sqlalchemy.orm import relationship

from app.core.db import Base

class NhanVien(Base):
    __tablename__ = 'NhanVien'

    IdNV = Column(UUID, primary_key=True)
    CCCD = Column(String, nullable=False)
    HoTen = Column(String, nullable=False)
    DiaChi = Column(String, nullable=False)
    SDT = Column(String, nullable=False)
    Gmail = Column(String, nullable=False)
    DiemDG = Column(Integer, default=100)
    TrangThai = Column(Boolean, default=True)

    schedules = relationship('LichLamViec', back_populates='mechanic')
    mechanic_list = relationship('DSNV', back_populates='mechanic')

class LichLamViec(Base):
    __tablename__ = 'LichLamViec'

    IdLLV = Column(UUID, primary_key=True)
    TGBD = Column(DATETIME, nullable=False)
    TGKT = Column(DATETIME, nullable=False)

    IdNV = Column(UUID, ForeignKey('NhanVien.IdNV'))

    mechanic = relationship('NhanVien', back_populates='schedules')

class KhachHang(Base):
    __tablename__ = 'KhachHang'

    IdKH = Column(UUID, primary_key=True)
    CCCD = Column(String, nullable=False)
    HoTen = Column(String, nullable=False)
    DiaChi = Column(String, nullable=False)
    SDT = Column(String, nullable=False)
    Gmail = Column(String, nullable=False)

    requests = relationship('PhieuThongTin', back_populates='customer')
    ac_list = relationship('ML_KH', back_populates='customer')

class PhieuThongTin(Base):
    __tablename__ = 'PhieuThongTin'

    IdPhieu = Column(UUID, primary_key=True)
    LichHen = Column(DATETIME)
    TGBD = Column(DATETIME)
    TGKT = Column(DATETIME)

    IdKH = Column(UUID, ForeignKey('KhachHang.IdKH'))

    customer = relationship('KhachHang', back_populates='requests')
    service_detail = relationship('CTDV', back_populates='request')

class NhaCC(Base):
    __tablename__ = 'NhaCC'

    IdCC = Column(UUID, primary_key=True)
    Ten = Column(String)

    # List of air conditioners from the supplier
    ac_list = relationship('MayLanh', back_populates='supplier') 
    # List of spare parts from the supplier
    sp_list = relationship('LK_NCC', back_populates='supplier')

class MayLanh(Base):
    __tablename__ = 'MayLanh'

    IdML = Column(UUID, primary_key=True)
    Ten = Column(String)
    DonGia = Column(MONEY)

    IdCC = Column(UUID, ForeignKey('NhaCC.IdCC'))

    supplier = relationship('NhaCC', back_populates='ac_list')
    ac_list = relationship('ML_KH', back_populates='air_conditioner')
    service_detail = relationship('CTDV', back_populates='air_conditioner')

class ML_KH(Base):
    __tablename__ = 'ML_KH'

    IdMLKH = Column(UUID, primary_key=True)
    IdML = Column(UUID, ForeignKey('MayLanh.IdML'))
    IdKH = Column(UUID, ForeignKey('KhachHang.IdKH'))
    MaSo = Column(Integer)
    
    customer = relationship('KhachHang', back_populates='ac_list')
    air_conditioner = relationship('MayLanh', back_populates='ac_list')
    ac_list = relationship('DSML', back_populates='customer_ac')

class LinhKien(Base):
    __tablename__ = 'LinhKien'

    IdLK = Column(UUID, primary_key=True)
    Ten = Column(String)

    sp_list = relationship('LK_NCC', back_populates='spare_part')

class LK_NCC(Base):
    __tablename__ = 'LK_NCC'
    
    IdLKCC = Column(UUID, primary_key=True)

    IdLK = Column(UUID, ForeignKey('LinhKien.IdLK'))
    IdCC = Column(UUID, ForeignKey('NhaCC.IdCC'))

    DonGia = Column(MONEY)

    spare_part = relationship('LinhKien', back_populates='sp_list')
    supplier = relationship('NhaCC', back_populates='sp_list')
    sp_list = relationship('DSLK', back_populates='sp_supplier')

    price_history = relationship('LSG_LK', back_populates='sp_supplier')

class LSG_LK(Base):
    __tablename__ = 'LSG_LK'

    IdLKCC = Column(UUID, ForeignKey('LK_NCC.IdLKCC'), primary_key=True)
    ThoiGian = Column(DATETIME, primary_key=True)
    DonGia = Column(MONEY)

    # Spare part from the supplier
    sp_supplier = relationship('LK_NCC', back_populates='price_history')

class DichVu(Base):
    __tablename__ = 'DichVu'

    IdDV = Column(UUID, primary_key=True)
    Ten = Column(String)
    DonGia = Column(MONEY)
    KhoiLuong = Column(Float)

    price_history = relationship('LSG_DV', back_populates='service')
    service_detail = relationship('CTDV', back_populates='service')

class LSG_DV(Base):
    __tablename__ = 'LSG_DV'

    IdDV = Column(UUID, ForeignKey('DichVu.IdDV'), primary_key=True)
    ThoiGian = Column(DATETIME, primary_key=True)
    DonGia = Column(MONEY)

    service = relationship('DichVu', back_populates='price_history')

class CTDV(Base):
    __tablename__ = 'CTDV'

    IdCTDV = Column(UUID, primary_key=True)
    IdPhieu = Column(UUID, ForeignKey('PhieuThongTin.IdPhieu'))
    IdDV = Column(UUID, ForeignKey('DichVu.IdDV'))
    IdML = Column(UUID, ForeignKey('MayLanh.IdML'))
    Soluong = Column(Integer)
    TrangThai = Column(Boolean)

    air_conditioner = relationship('MayLanh', back_populates='service_detail')
    request = relationship('PhieuThongTin', back_populates='service_detail')
    service = relationship('DichVu', back_populates='service_detail')
    mechanic_list = relationship('DSNV', back_populates='service_detail')
    ac_list = relationship('DSML', back_populates='service_detail')

class DSNV(Base):
    __tablename__ = 'DSNV'
    
    IdDSNV = Column(UUID, primary_key=True)
    IdCTDV = Column(UUID, ForeignKey('CTDV.IdCTDV'))
    IdNV = Column(UUID, ForeignKey('NhanVien.IdNV'))

    service_detail = relationship('CTDV', back_populates='mechanic_list')
    mechanic = relationship('NhanVien', back_populates='mechanic_list')
    maintainance = relationship('BaoTri', back_populates='mechanic_list')

class DSML(Base):
    __tablename__ = 'DSML'
    
    IdDSML = Column(UUID, primary_key=True)
    IdCTDV = Column(UUID, ForeignKey('CTDV.IdCTDV'))
    IdMLKH = Column(UUID, ForeignKey('ML_KH.IdML'))

    service_detail = relationship('CTDV', back_populates='ac_list')
    customer_ac = relationship('ML_KH', back_populates='ac_list')
    ac_list = relationship('BaoTri', back_populates='air_conditioner')

class BaoTri(Base):
    __tablename__ = 'BaoTri'

    IdBT = Column(UUID, primary_key=True)
    IdDSNV = Column(UUID, ForeignKey('DSNV.IdDSNV'))
    IdDSML = Column(UUID, ForeignKey('DSML.IdDSML'))
    DiemDG = Column(Integer)

    mechanic_list = relationship('DSNV', back_populates='maintainance')
    air_conditioner = relationship('DSML', back_populates='ac_list')
    sp_list = relationship('DSLK', back_populates='maintainance')
    feedback = relationship('PhanHoi', back_populates='maintainance')

class DSLK(Base):
    __tablename__ = 'DSLK'

    IdDSLK = Column(UUID, primary_key=True)
    IdBT = Column(UUID, ForeignKey('BaoTri.IdBT'))
    IdLKCC = Column(UUID, ForeignKey('LK_NCC.IdLKCC'))
    SoLuong = Column(Integer)

    maintainance = relationship('BaoTri', back_populates='sp_list')
    sp_supplier = relationship('LK_NCC', back_populates='sp_list')  

class PhanHoi(Base):
    __tablename__ = 'PhanHoi'

    IdPH = Column(UUID, primary_key=True)
    NoiDung = Column(String)
    
    IdBT = Column(UUID, ForeignKey('BaoTri.IdBT'))

    maintainance = relationship('BaoTri', back_populates='feedback')