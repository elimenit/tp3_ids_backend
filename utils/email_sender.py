import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from email.mime.image     import MIMEImage
 
FRONTEND_URL = "http://localhost:10000"  
 
 
def enviar_email_reserva(destinatario, nombre, reserva_id,
                          fecha, qr_path, qr_token):
    """
    Envia el email de confirmacion con:
    - Datos de la reservacion
    - Imagen del QR adjunta
    - Link para cancelar (usa el token, NUNCA el ID)
 
    Las credenciales vienen del .env, NUNCA van escritas en el codigo.
    """
 
    # Leer credenciales del archivo .env
    remitente = os.getenv("EMAIL_USER")
    password  = os.getenv("EMAIL_PASS")
 
    # Construir el mensaje
    mensaje            = MIMEMultipart()
    mensaje["From"]    = remitente
    mensaje["To"]      = destinatario
    mensaje["Subject"] = f"Confirmacion de reservacion #{reserva_id}"
 
    # Link de cancelacion usando el token (no el ID)
    link_cancelar = f"{FRONTEND_URL}/reservations/cancelar?token={qr_token}"
 
    # Cuerpo del email en HTML
    cuerpo = f"""
    <h2>Hola {nombre}!</h2>
    <p>Tu reservacion <strong>#{reserva_id}</strong> fue registrada.</p>
    <p><strong>Fecha y hora:</strong> {fecha}</p>
    <p>Presenta el QR adjunto al llegar al restaurante.</p>
    <br>
    <a href="{link_cancelar}"
       style="background:#dc3545; color:white; padding:10px 20px;
              border-radius:6px; text-decoration:none; font-weight:bold">
       Cancelar mi reservacion
    </a>
    <br><br>
    <p style="color:#888; font-size:12px">
      Si no realizaste esta reservacion ignora este email.
    </p>
    """
    mensaje.attach(MIMEText(cuerpo, "html"))
 
    # Adjuntar la imagen del QR
    with open(qr_path, "rb") as archivo:
        imagen_qr = MIMEImage(archivo.read())
        imagen_qr.add_header(
            "Content-Disposition",
            "attachment",
            filename=f"reserva_{reserva_id}.png"
        )
        mensaje.attach(imagen_qr)
 
    # Enviar usando Gmail con App Password
    with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
        servidor.starttls()                  # activa cifrado TLS
        servidor.login(remitente, password)  # autenticacion
        servidor.send_message(mensaje)       # envio
