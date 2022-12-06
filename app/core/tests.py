import smtplib
from email.mime.text import MIMEText

from config import settings


def send_email():
    try:
        # Establecemos conexion con el servidor smtp de gmail
        # Conectamos al servidor
        mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        """Ehlo es la etapa del protocolo smtp en la que un servidor se presenta entre si. Y verifica
         que no hay errores en el proceso"""
        print(mailServer.ehlo())
        """TLS sirve para mejorar la seguridad de las conexiones SMTP igual que SSL y evitar hackeos"""
        mailServer.starttls()
        print(mailServer.ehlo())
        mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print('Conectado...')

        email_to = 'esdeciencia@gmail.com'
        # Construimos el mensaje simple
        mensaje = MIMEText("""Este es el mensaje
        de las narices""")
        mensaje['From'] = settings.EMAIL_HOST_USER
        mensaje['To'] = email_to
        mensaje['Subject'] = "Tienes un correo"
        # Envio del mensaje
        mailServer.sendmail(settings.EMAIL_HOST_USER,
                            email_to,
                            mensaje.as_string())
    except Exception as e:
        print(e)


send_email()
