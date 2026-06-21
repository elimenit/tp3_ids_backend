import qrcode
import os
 
FRONTEND_URL = "http://localhost:10000"  
 
def generar_qr(reserva_id, qr_token):
    """
    Genera el QR con la URL de cancelacion y guarda la imagen.
 
    El QR codifica una URL completa, no solo el ID.
    Asi cuando el admin escanea el QR en el local
    abre directamente la pantalla de la reservacion.
 
    Devuelve la ruta del archivo generado.
    """
 
    # La URL que va codificada adentro del QR
    url = f"{FRONTEND_URL}/reservations/cancelar?token={qr_token}"
 
    # Crear la imagen del QR
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    imagen = qr.make_image(fill_color="black", back_color="white")
 
    # Crear la carpeta si no existe
    carpeta = "static/qr_codes"
    os.makedirs(carpeta, exist_ok=True)
    # exist_ok=True evita error si la carpeta ya existe
 
    # Guardar la imagen
    ruta = f"{carpeta}/reserva_{reserva_id}.png"
    imagen.save(ruta)
 
    return ruta
 
