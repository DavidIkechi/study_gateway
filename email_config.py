from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
import os


conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv('EMAIL'),
    MAIL_PASSWORD = os.getenv('PASS'),
    MAIL_FROM = os.getenv('EMAIL'),
    MAIL_PORT = 587,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_FROM_NAME="Study Gateway",
    MAIL_STARTTLS = True,
    USE_CREDENTIALS = True,
    MAIL_SSL_TLS= False,
    VALIDATE_CERTS = True,
    TEMPLATE_FOLDER='templates'
)

