import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO
from typing import List
from ..config import settings
from datetime import datetime

def send_waiver_email(
    user_email: str,
    user_name: str,
    qr_code: str,
    pdf_buffer: BytesIO,
    relatives: List[dict]
) -> bool:
    """
    Enviar email con PDF del waiver adjunto
    """
    try:
        # Configurar el mensaje
        msg = MIMEMultipart()
        msg['From'] = settings.smtp_user
        msg['To'] = user_email
        msg['Subject'] = f"Waiver KidsFun - {user_name}"

        # Cuerpo del email
        relatives_text = "\n".join([f"• {relative['name']} ({relative['age']} años)" for relative in relatives])
        
        body = f"""
        Hola {user_name},

        Tu waiver ha sido creado exitosamente para KidsFun.

        **Información del Waiver:**
        - Código QR: {qr_code}
        - Fecha de creación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        - Válido por: 24 horas

        **Familiares registrados:**
        {relatives_text}

        **Instrucciones:**
        1. Presenta este PDF al llegar a KidsFun
        2. El código QR será escaneado para validar tu entrada
        3. Este waiver es válido por 24 horas desde su creación

        Si tienes alguna pregunta, no dudes en contactarnos.

        Saludos,
        Equipo KidsFun
        """

        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # Adjuntar PDF
        pdf_buffer.seek(0)
        pdf_attachment = MIMEBase('application', 'pdf')
        pdf_attachment.set_payload(pdf_buffer.read())
        encoders.encode_base64(pdf_attachment)
        pdf_attachment.add_header(
            'Content-Disposition',
            f'attachment; filename=waiver_{user_name}_{qr_code}.pdf'
        )
        msg.attach(pdf_attachment)

        # Enviar email
        server = smtplib.SMTP(settings.smtp_host, settings.smtp_port)
        server.starttls()
        server.login(settings.smtp_user, settings.smtp_password)
        text = msg.as_string()
        server.sendmail(settings.smtp_user, user_email, text)
        server.quit()

        return True

    except Exception as e:
        print(f"Error enviando email a {user_email}: {str(e)}")
        return False 