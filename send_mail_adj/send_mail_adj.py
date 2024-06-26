import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from credenciales import *


def adjuntar_archivo(msg, filepath):
    filename = filepath.split("/")[-1]
    with open(filepath, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={filename}")
        msg.attach(part)


usuario = "Juan [desde Python]"
asunto = "Mensaje enviado con Python"
destinatarios = ["personal@gmail.com"]
mensaje = "Este correo tiene archivos adjuntos."

# Crea la instancia del mensaje
msg = MIMEMultipart()
msg["From"] = usuario
msg["Subject"] = asunto
msg["To"] = ", ".join(destinatarios)
msg.attach(MIMEText(mensaje))

# Adjuntamos los documentos
adjuntar_archivo(msg, "send_mail_adj/files/ok.png")
adjuntar_archivo(msg, "send_mail_adj/files/notas.txt")
adjuntar_archivo(msg, "send_mail_adj/files/doc.pdf")
adjuntar_archivo(msg, "send_mail_adj/files/libro.xlsx")

# Crea la conexión y envía el correo
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(USER_MAIL, PASSWORD)
    server.sendmail(USER_MAIL, destinatarios, msg.as_string())
    print(f"Correo enviado.")
