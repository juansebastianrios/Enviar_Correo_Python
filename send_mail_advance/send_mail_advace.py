import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import pandas as pd
from credenciales import *

CCO_EMAILS = []


def send_email(destinatarios, usuario, asunto, mensaje):
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(USER_MAIL, PASSWORD)

        msg = MIMEMultipart()
        msg["From"] = usuario
        msg["Subject"] = asunto
        msg["To"] = ", ".join(destinatarios)
        msg["Bcc"] = ", ".join(CCO_EMAILS)
        msg.attach(MIMEText(mensaje))

        with open("send_mail_advance/firma.png", "rb") as archivo_firma:
            firma_imagen = MIMEImage(archivo_firma.read())
            firma_imagen.add_header(
                "Content-Disposition",
                "attachment",
                filename="send_mail_advance/firma.png",
            )
            msg.attach(firma_imagen)

        server.sendmail(USER_MAIL, destinatarios + CCO_EMAILS, msg.as_string())


if __name__ == "__main__":
    # Crear un csv con encabezados [nombre, email, deuda]
    df = pd.read_csv("send_mail_advance/info.csv", delimiter=";")
    for indice, fila in df.iterrows():
        nombre = fila.loc["nombre"]
        email = fila.loc["email"]
        deuda = fila.loc["deuda"]

        send_email(
            usuario="Cobrador profesional",
            destinatarios=[email],
            asunto="Pague su deuda",
            mensaje=f"Estimado {nombre},\n\nLe comunico que debe un monto de ${deuda}.",
        )

        print(f"Mensaje enviado a {email}.")
