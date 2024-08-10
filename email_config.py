from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
import os


conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv('EMAIL'),
    MAIL_PASSWORD = os.getenv('PASS'),
    MAIL_FROM = os.getenv('EMAIL'),
    MAIL_PORT = 465,
    MAIL_SERVER = 'smtp.zoho.com',
    MAIL_FROM_NAME="Study Gateway",
    MAIL_STARTTLS = False,
    USE_CREDENTIALS = True,
    MAIL_SSL_TLS= True,
    VALIDATE_CERTS = True,
    TEMPLATE_FOLDER='templates'
)

