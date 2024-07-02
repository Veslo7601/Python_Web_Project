# PhotoShare/services/qrcode_service.py

import qrcode
import cloudinary
import cloudinary.uploader
from io import BytesIO
from PhotoShare.conf.config import settings
from urllib.parse import unquote

# Настройка Cloudinary
cloudinary.config(
    cloud_name=settings.CLD_NAME,
    api_key=settings.CLD_API_KEY,
    api_secret=settings.CLD_API_SECRET,
    secure=True,
)

async def generate_qr_code(image_url: str) -> str:
    # Создание QR кода
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(image_url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # Сохранение QR кода в BytesIO (в оперативной памяти)
    img_bytes = BytesIO()
    img.save(img_bytes)
    img_bytes.seek(0)  # Перемотка BytesIO в начало, чтобы его можно было прочитать

    # Загрузка QR кода в Cloudinary и получение его URL
    res = cloudinary.uploader.upload(img_bytes, public_id=f"qrcodes/{image_url.split('/')[-1]}", overwrite=True)
    qr_code_url = res.get("url")

    return qr_code_url
