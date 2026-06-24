import qrcode
import os
from constants import FRONTEND_URL
 
def generar_qr(reserva_id, qr_token):
    """
    Genera el QR con la URL de cancelacion y guarda la imagen.
 
    El QR codifica una URL completa, no solo el ID.
    Asi cuando el admin escanea el QR en el local
    abre directamente la pantalla de la reservacion.
 
    Devuelve la ruta del archivo generado.
    """
    url = f"{FRONTEND_URL}/reservations/confirmar?token={qr_token}"

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    imagen = qr.make_image(fill_color="black", back_color="white")

    carpeta = "static/qr_codes"
    os.makedirs(carpeta, exist_ok=True)
    ruta = f"{carpeta}/reserva_{reserva_id}.png"
    imagen.save(ruta)
 
    return ruta
 
