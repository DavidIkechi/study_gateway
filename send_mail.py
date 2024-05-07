from email_config import conf
from schemas.email_schema import EmailSchema
from fastapi import BackgroundTasks
from typing import List, Dict, Any
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType


from db.main_model import UserModel
import os

def generate_verification_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=1440)
    token_data = {'sub': email, 'exp': expire}
    token = jwt.encode(token_data, os.getenv('SECRET'), algorithm='HS256')
    return token

async def send_verification_email(email_address: str, background_tasks: BackgroundTasks):
    token = generate_verification_token(email_address)

    # Prepare email details
    url = os.getenv("HOST_URL")
    emails: EmailSchema = {
        "body": {
            "url": f"{url}verify_mail?token={token}",
            "email_address": "Esteem User"
        } 
    }
    # Define message structure
    message = MessageSchema(
        subject="Email Verification",
        recipients=[email_address],  # Send to single address
        template_body=emails.get('body'),
        subtype=MessageType.html
    )

    # Send email in background task
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message=message, template_name='password_verification.html')

    return token

async def send_verification_code(email_address: str, code: str, background_tasks: BackgroundTasks):
    token = generate_verification_token(email_address)

    # Prepare email details
    url = os.getenv("HOST_URL")
    emails: EmailSchema  = {
        "body": {
            "sent_code": code,
            "email_address": "Esteem User"
        } 
    }
    # Define message structure
    message = MessageSchema(
        subject="Password Reset",
        recipients=[email_address],  # Send to single address
        template_body=emails.get('body'),
        subtype=MessageType.html
    )

    # Send email in background task
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message=message, template_name='verification_code.html')

    return token