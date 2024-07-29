import sys
sys.path.append("..")
from utils import *
from db.session import Session
from sqlalchemy.orm import Session, load_only, relationship
from exceptions import (
    BadExceptions, 
    NotFoundException, 
    ServerErrorException, 
    NotAuthorizedException,
    ForbiddenException
)
from db.main_model import WaitlistModel
from argon2 import PasswordHasher
from send_mail import *
from auth_token import *
import pyotp
from datetime import datetime, timedelta
from simpleotp import OTP
from fastapi.responses import StreamingResponse
import csv
from io import StringIO
import os

def check_mail(db, email, new_user= False):
    get_user = WaitlistModel.check_email(db, email)
    if new_user:
        if get_user is not None:
            raise BadExceptions(detail=f"Email {email} already on waitlist.")
    else:
        if get_user is None:
            raise NotFoundException(detail=f"User with this email {email} does not exist.")
        
    return get_user
        

async def create_waitlist(db, user, backtasks):
    # check to see if the email address already exists
    check_waitlist =  check_mail(db, user.email_address, new_user=True)
    # check passwords.
    user_dict = user.dict(exclude_unset = True)
    create_new_waitlist = WaitlistModel.create_waitlist(user_dict)
    db.add(create_new_waitlist)
    # send verification mail notification
    # await send_verification_email(user.email_address, backtasks)
    return create_new_waitlist


async def delete_waitlist(db, email_address, backtasks):
    # check to see if the email address already exists
    check_waitlist =  check_mail(db, email_address)
    
    db.delete(check_waitlist)
    # send verification mail notification
    # await send_verification_email(email_address, backtasks)
    return email_address

def get_all_waitlist(db):
    waitlists = WaitlistModel.get_waitlists(db)
    emails = [entry.email_address for entry in waitlists]

    # Create a CSV file in memory
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Email_Address'])
    writer.writerows([[email] for email in emails])
    output.seek(0)
    
    response = StreamingResponse(output, media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=waitlist_emails.csv"
    
    return response
    