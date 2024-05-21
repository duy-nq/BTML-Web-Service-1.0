from datetime import datetime
import hashlib
import hmac
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from app.crud.crud_request import get_phieu_thong_tin
from app.crud.crud_service import get_all_dich_vu
from app.crud.crud_sp import get_all_linh_kien
from app.crud.crud_sp_supplier import get_all_lk_ncc
from app.schemas import Payment, TongTienDV, TongTienLK
from app.core.db import get_db
from app.vnpay import vnpay

VNPAY_RETURN_URL = 'http://127.0.0.1:8000/api/v1/payment_return'
VNPAY_PAYMENT_URL = 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html'  
VNPAY_API_URL = 'https://sandbox.vnpayment.vn/merchant_webapi/merchant.html'
VNPAY_TMN_CODE = 'SVFJFLA2'  
VNPAY_HASH_SECRET_KEY = "4PKOX3VB14FSOES1JSMIJWEEZT5TBTHH"

router = APIRouter(tags=['ThanhToan'])


@router.get('/total-service/{id}', response_model=list[TongTienDV])
async def read_total_service(IdPhieu: str, db = Depends(get_db)):
    try:
        phieu = get_phieu_thong_tin(db, IdPhieu=IdPhieu)
        if phieu is None:
            raise HTTPException(status_code=404, detail="Phieu khong ton tai")
        
        dichvu = get_all_dich_vu(db)
        if dichvu is None:
            raise HTTPException(status_code=404, detail="Khong the tai dich vu")
        
        results = []

        id = ''
        ten = ''
        don_gia = 0
        so_luong = 0
        tong_tien = 0
        
        for ct in phieu.service_detail:
            id = ct.IdDV
            for dv in dichvu:
                if ct.IdDV == dv.IdDV:
                    ten = dv.Ten
                    don_gia = dv.DonGia
                    break
            so_luong = ct.SoLuong
            tong_tien = so_luong * don_gia

            results.append(TongTienDV(IdDV=id, Ten=ten, DonGia=don_gia, SoLuong=so_luong, TongTien=tong_tien))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Chua them dich vu hoac nhap sai id")
    
    print(results)
    
    if len(results) == 0:
        raise HTTPException(status_code=404, detail="Khong co dich vu nao")
    return results

@router.get('/total-sp/{id}', response_model=list[TongTienLK])
async def read_total_sp(IdPhieu: str, db = Depends(get_db)):
    try:
        phieu = get_phieu_thong_tin(db, IdPhieu=IdPhieu)
        if phieu is None:
            raise HTTPException(status_code=404, detail="Phieu khong ton tai")
        
        lkncc = get_all_lk_ncc(db)
        if lkncc is None:
            raise HTTPException(status_code=404, detail="Khong the tai lkncc")
        
        linhkien = get_all_linh_kien(db)
        if linhkien is None:
            raise HTTPException(status_code=404, detail="Khong the tai linh kien")
        
        results = []

        id = ''
        ten = ''
        don_gia = 0
        so_luong = 0
        tong_tien = 0

        ctdv = phieu.service_detail

        for ct in ctdv:
            dsbt = ct.maintenance
            for bt in dsbt:
                dslk = bt.sp_list
                for lk in dslk:
                    id = lk.IdLKCC
                    for lkcc in lkncc:
                        if lk.IdLKCC == lkcc.IdLKCC:
                            for item in linhkien:
                                if lkcc.IdLK == item.IdLK:
                                    ten = item.Ten
                                    break
                            break
                        don_gia = lkcc.DonGia
                            
                    so_luong = lk.SoLuong
                    tong_tien = so_luong * don_gia

                    print(results)

                    results.append(TongTienLK(IdLK=id, Ten=ten, DonGia=don_gia, SoLuong=so_luong, TongTien=tong_tien))

    except Exception as e:
        raise HTTPException(status_code=500, detail="Chua them linh kien hoac nhap sai id")
        
    if len(results) == 0:
        raise HTTPException(status_code=404, detail="Khong co linh kien nao")
    return results

def generate_secure_hash(data, secret_key):
    sorted_data = sorted(data.items())
    query_string = '&'.join(['{}={}'.format(k, v) for k, v in sorted_data])
    hashed = hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha512)
    print(hashed.hexdigest().upper())
    return hashed.hexdigest().upper()

@router.post('/payment/', response_model=str)
async def payment(pay: Payment, db = Depends(get_db)):
    vnp = vnpay()

    vnp.requestData['vnp_Version'] = '2.1.0'
    vnp.requestData['vnp_Command'] = 'pay'
    vnp.requestData['vnp_TmnCode'] = VNPAY_TMN_CODE
    vnp.requestData['vnp_Amount'] = int(pay.ThanhTien*100)
    vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')    
    vnp.requestData['vnp_CurrCode'] = 'VND'
    vnp.requestData['vnp_TxnRef'] = pay.IdPhieu + '-' + datetime.now().strftime('%Y%m%d%H%M%S')
    vnp.requestData['vnp_OrderInfo'] = pay.NoiDung
    vnp.requestData['vnp_OrderType'] = 'billpayment'
    vnp.requestData['vnp_Locale'] = 'vn'
    vnp.requestData['vnp_IpAddr'] = '192.168.1.101'
    vnp.requestData['vnp_ReturnUrl'] = VNPAY_RETURN_URL

    return vnp.get_payment_url(VNPAY_PAYMENT_URL, VNPAY_HASH_SECRET_KEY)

@router.get('/payment_return')
async def payment_return(
    vnp_Amount: str = Query(...),
    vnp_BankCode: str = Query(...),
    vnp_BankTranNo: str = Query(...),
    vnp_CardType: str = Query(...),
    vnp_OrderInfo: str = Query(...),
    vnp_PayDate: str = Query(...),
    vnp_ResponseCode: str = Query(...),
    vnp_TmnCode: str = Query(...),
    vnp_TransactionNo: str = Query(...),
    vnp_TransactionStatus: str = Query(...),
    vnp_TxnRef: str = Query(...),
    vnp_SecureHash: str = Query(...)
):
    vnp = vnpay()

    vnp.responseData['vnp_Amount'] = vnp_Amount
    vnp.responseData['vnp_BankCode'] = vnp_BankCode
    vnp.responseData['vnp_BankTranNo'] = vnp_BankTranNo
    vnp.responseData['vnp_CardType'] = vnp_CardType
    vnp.responseData['vnp_OrderInfo'] = vnp_OrderInfo
    vnp.responseData['vnp_PayDate'] = vnp_PayDate
    vnp.responseData['vnp_ResponseCode'] = vnp_ResponseCode
    vnp.responseData['vnp_TmnCode'] = vnp_TmnCode
    vnp.responseData['vnp_TransactionNo'] = vnp_TransactionNo
    vnp.responseData['vnp_TransactionStatus'] = vnp_TransactionStatus
    vnp.responseData['vnp_TxnRef'] = vnp_TxnRef
    vnp.responseData['vnp_SecureHash'] = vnp_SecureHash

    if vnp.validate_response(VNPAY_HASH_SECRET_KEY):
        return 'Thanh toan thanh cong'
    else:
        return 'Thanh toan that bai'