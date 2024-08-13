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

async def send_verification_email(user: UserModel, background_tasks: BackgroundTasks, mentor=False):
    token = generate_verification_token(user.email_address)

    # Prepare email details
    url = os.getenv("HOST_URL")
    if mentor:
        url = f"{url}/mentor/verify-user/{token}"
    else:
        url = f"{url}/verify-user/{token}"
    emails: EmailSchema = {
        "body": {
            "name": user.first_name,
            "url": f"{url}",
            "email_address": user.email_address
        } 
    }
    # Define message structure
    message = MessageSchema(
        subject="Account Verification",
        recipients=[user.email_address],  # Send to single address
        template_body=emails.get('body'),
        subtype=MessageType.html
    )

    # Send email in background task
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message=message, template_name='password_verification.html')

    return token

async def send_verification_code(user: UserModel, code: str, background_tasks: BackgroundTasks):
    token = generate_verification_token(user.email_address)

    # Prepare email details
    url = os.getenv("HOST_URL")
    emails: EmailSchema  = {
        "body": {
            "name": user.first_name,
            "sent_code": list(code),
            "email_address": user.email_address
        } 
    }
    # Define message structure
    message = MessageSchema(
        subject="Password Reset",
        recipients=[user.email_address],  # Send to single address
        template_body=emails.get('body'),
        subtype=MessageType.html
    )

    # Send email in background task
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message=message, template_name='verification_code.html')

    return token

async def welcome_email(user: UserModel, background_tasks: BackgroundTasks):
    # Prepare email details
    url = os.getenv("HOST_URL")
    emails: EmailSchema  = {
        "body": {
            "name": user.first_name,
            "url": url,
            "email_address": user.email_address
        } 
    }
    # Define message structure
    message = MessageSchema(
        subject="Welcome",
        recipients=[user.email_address],  # Send to single address
        template_body=emails.get('body'),
        subtype=MessageType.html
    )

    # Send email in background task
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message=message, template_name='welcome.html')

    return

async def connection_email(user: UserModel, mentor: UserModel, background_tasks: BackgroundTasks):
    # Prepare email details
    url = "https://slack.com/intl/en-in/"
    emails: EmailSchema  = {
        "body": {
            "name": user.first_name,
            "url": url,
            "email_address": user.email_address
        } 
    }
    # Define message structure
    message = MessageSchema(
        subject=f"Mentor-Mentee Slack Invitation from {mentor.first_name.title()}",
        recipients=[user.email_address],  # Send to single address
        template_body=emails.get('body'),
        subtype=MessageType.html
    )

    # Send email in background task
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message=message, template_name='mentor.html')

    return